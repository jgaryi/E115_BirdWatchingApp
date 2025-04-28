import os
import argparse
import hashlib
import glob
import pandas as pd
import chromadb
import requests

# Vertex AI
import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

# Langchain
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from semantic_splitter import SemanticChunker

# === Setup ===
GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_LOCATION = "us-central1"
CHROMADB_HOST = os.environ["CHROMADB_HOST"]
CHROMADB_PORT = os.environ["CHROMADB_PORT"]
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 256
INPUT_FOLDER = "input-datasets"
OUTPUT_FOLDER = "outputs"

vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)
embedding_model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL)


def generate_text_embeddings(chunks, dimensionality: int = 256, batch_size=250):
    """Generate text embeddings for a list of text chunks."""
    all_embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        inputs = [TextEmbeddingInput(text, "RETRIEVAL_DOCUMENT") for text in batch]
        kwargs = dict(output_dimensionality=dimensionality)
        embeddings = embedding_model.get_embeddings(inputs, **kwargs)
        all_embeddings.extend([e.values for e in embeddings])
    return all_embeddings


def download():
    """Download text datasets from GCS bucket."""
    print("Downloading dataset from GCS bucket...")

    # Folder to save the downloaded files
    target_folder = os.path.join(INPUT_FOLDER, "books")
    os.makedirs(target_folder, exist_ok=True)

    # List of text files in the GCS bucket
    file_names = [
        "bird_description-Andigena%20hypoglauca.txt", 
        "bird_description-Aulacorhynchus%20coeruleicinctis.txt", 
        "bird_description-Gallinago%20jamesoni.txt", 
        "bird_description-Hapalopsittaca%20melanotis.txt", 
        "bird_description-Pionus%20tumultuosus.txt",
        "bird_description-Pipile%20cumanensis.txt", 
        "bird_description-Rupicola%20peruvianus.txt", 
        "bird_description-Tinamus%20osgoodi.txt", 
        "bird_description-Doliornis%20sclateri.txt"
    ]

    base_url = "https://storage.googleapis.com/birdwatching_app/input-datasets/books/"

    for file_name in file_names:
        url = f"{base_url}{file_name}"
        local_path = os.path.join(target_folder, file_name)

        # Skip download if file already exists
        if os.path.exists(local_path):
            print(f"Skipping {file_name} (already exists)")
            continue

        print(f"Downloading {file_name}...")
        r = requests.get(url)
        if r.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(r.content)
            print(f"Saved to {local_path}")
        else:
            print(f"Failed to download {file_name} (status code: {r.status_code})")

    print("All available files downloaded.")


def chunk(method="char-split"):
    """Chunk text files using different splitting strategies."""
    print("Chunking text...")

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    text_files = glob.glob(os.path.join(INPUT_FOLDER, "books", "*.txt"))
    print("Files found:", len(text_files))

    for text_file in text_files:
        filename = os.path.basename(text_file)
        book_name = filename.split(".")[0]

        with open(text_file) as f:
            input_text = f.read()

        if method == "char-split":
            text_splitter = CharacterTextSplitter(chunk_size=350, chunk_overlap=20)
        elif method == "recursive-split":
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=350)
        elif method == "semantic-split":
            text_splitter = SemanticChunker(embedding_function=generate_text_embeddings)
        else:
            raise ValueError(f"Unsupported chunk_type: {method}")

        text_chunks = [doc.page_content for doc in text_splitter.create_documents([input_text])]
        print(f"Created {len(text_chunks)} chunks for {book_name}")

        df = pd.DataFrame(text_chunks, columns=["chunk"])
        df["book"] = book_name

        output_file = os.path.join(OUTPUT_FOLDER, f"chunks-{method}-{book_name}.jsonl")
        df.to_json(output_file, orient="records", lines=True)
        print("Saved chunks to:", output_file)


def embed(method="char-split"):
    """Generate embeddings for previously chunked text files."""
    print("Embedding text chunks...")

    jsonl_files = glob.glob(os.path.join(OUTPUT_FOLDER, f"chunks-{method}-*.jsonl"))
    print("Files found:", len(jsonl_files))

    for jsonl_file in jsonl_files:
        df = pd.read_json(jsonl_file, lines=True)
        print(f"Embedding {len(df)} chunks from {jsonl_file}")

        chunks = df["chunk"].tolist()
        if method == "semantic-split":
            embeddings = generate_text_embeddings(chunks, batch_size=15)
        else:
            embeddings = generate_text_embeddings(chunks, batch_size=100)

        df["embedding"] = embeddings

        output_file = jsonl_file.replace("chunks-", "embeddings-")
        df.to_json(output_file, orient="records", lines=True)
        print("Saved embeddings to:", output_file)


def load(method="char-split"):
    """Load generated embeddings into ChromaDB."""
    print("Loading embeddings into ChromaDB...")

    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    collection_name = f"{method}-collection"

    try:
        client.delete_collection(name=collection_name)
        print(f"Deleted old collection '{collection_name}'")
    except:
        print(f"No existing collection '{collection_name}' to delete.")

    collection = client.create_collection(name=collection_name, metadata={"hnsw:space": "cosine"})
    print(f"Created new collection '{collection_name}'")

    jsonl_files = glob.glob(os.path.join(OUTPUT_FOLDER, f"embeddings-{method}-*.jsonl"))
    for jsonl_file in jsonl_files:
        df = pd.read_json(jsonl_file, lines=True)

        df["id"] = df.index.astype(str)
        hashed = df["book"].apply(lambda x: hashlib.sha256(x.encode()).hexdigest()[:16])
        df["id"] = hashed + "-" + df["id"]

        collection.add(
            ids=df["id"].tolist(),
            documents=df["chunk"].tolist(),
            metadatas=[{"book": b} for b in df["book"]],
            embeddings=df["embedding"].tolist()
        )
        print(f"Loaded {len(df)} records from {jsonl_file} into ChromaDB.")


def main():
    """Main CLI entry point for vector database operations."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true", help="Download the dataset")
    parser.add_argument("--chunk", action="store_true", help="Chunk text files")
    parser.add_argument("--embed", action="store_true", help="Embed chunks")
    parser.add_argument("--load", action="store_true", help="Load embeddings into vector db")
    parser.add_argument("--chunk_type", default="char-split", help="char-split | recursive-split | semantic-split")
    args = parser.parse_args()

    if args.download:
        download()

    chunk_files_exist = glob.glob(os.path.join(OUTPUT_FOLDER, f"chunks-{args.chunk_type}-*.jsonl"))
    if args.chunk:
        if chunk_files_exist:
            print(f"Skipping chunking — chunks for '{args.chunk_type}' already exist.")
        else:
            chunk(args.chunk_type)

    embedding_files_exist = glob.glob(os.path.join(OUTPUT_FOLDER, f"embeddings-{args.chunk_type}-*.jsonl"))
    if args.embed:
        if embedding_files_exist:
            print(f"Skipping embedding — embeddings for '{args.chunk_type}' already exist.")
        else:
            embed(args.chunk_type)

    # Re-check embeddings after embedding step
    embedding_files_exist = glob.glob(os.path.join(OUTPUT_FOLDER, f"embeddings-{args.chunk_type}-*.jsonl"))

    if args.load:
        if not embedding_files_exist:
            print("Cannot load: no embedding files found. Run with --embed first.")
        else:
            load(args.chunk_type)


if __name__ == "__main__":
    main()

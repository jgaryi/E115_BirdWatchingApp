"""Utilities for bird information retrieval using embeddings and function calling."""

from vertexai.generative_models import FunctionDeclaration, Tool, Part
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

# Embedding setup
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 256
embedding_model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL)

def generate_query_embedding(query: str):
    """Generate a text embedding vector from a query string."""
    query_embedding_inputs = [TextEmbeddingInput(task_type='RETRIEVAL_DOCUMENT', text=query)]
    kwargs = {"output_dimensionality": EMBEDDING_DIMENSION}
    embeddings = embedding_model.get_embeddings(query_embedding_inputs, **kwargs)
    return embeddings[0].values

# Define the tool function that the LLM can call
get_bird_info_func = FunctionDeclaration(
    name="get_bird_info",
    description="Search bird knowledge base using text embeddings",
    parameters={
        "type": "object",
        "properties": {
            "search_content": {
                "type": "string",
                "description": "The search query to retrieve bird-related information."
            },
        },
        "required": ["search_content"],
    },
)

# Actual tool function implementation
def get_bird_info(search_content, collection, embed_func):
    """Retrieve bird-related information from the local knowledge base."""
    query_embedding = embed_func(search_content)
    results = collection.query(query_embeddings=[query_embedding], n_results=10)
    local_results = results["documents"][0] if results["documents"] else []

    insufficient = len(local_results) < 3 or all(len(doc.strip()) < 50 for doc in local_results)

    if insufficient:
        print("Local results may be insufficient — no external fallback used.")
    combined_results = local_results

    return "\n".join(combined_results)

# Register the tool
bird_expert_tool = Tool(function_declarations=[get_bird_info_func])

def execute_function_calls(function_calls, collection, embed_func):
    """Execute LLM function calls and wrap responses in Part objects."""
    parts = []
    for function_call in function_calls:
        if function_call.name == "get_bird_info":
            print("\n[Agent TOOL CALL] — Bird info tool triggered")
            print(f"Search content requested: '{function_call.args['search_content']}'\n")
            response = get_bird_info(function_call.args["search_content"], collection, embed_func)
            print(f"[Agent TOOL RESPONSE] — Retrieved {len(response)} characters of data.\n")

            parts.append(
                Part.from_function_response(
                    name=function_call.name,
                    response={"content": response},
                )
            )
    return parts

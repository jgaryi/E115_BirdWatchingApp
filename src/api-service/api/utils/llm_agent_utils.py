
from vertexai.generative_models import GenerativeModel, ChatSession, Part
import uuid
import chromadb
from vertexai.generative_models import (
    Content,
    Part,
    GenerationConfig,
    # ToolConfig,
    ChatSession,
    GenerativeModel
)
from fastapi import HTTPException

GENERATIVE_MODEL = "gemini-2.0-flash"
generative_model = GenerativeModel(GENERATIVE_MODEL)


# ----------------------
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
import os

EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 256


embedding_model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL)



from api.utils.agent_tools import bird_expert_tool, execute_function_calls

CHROMADB_HOST = os.environ["CHROMADB_HOST"]
CHROMADB_PORT = os.environ["CHROMADB_PORT"]


chat_sessions = {}

def generate_query_embedding(query):
    query_embedding_inputs = [TextEmbeddingInput(task_type='RETRIEVAL_DOCUMENT', text=query)]
    kwargs = dict(output_dimensionality=EMBEDDING_DIMENSION) if EMBEDDING_DIMENSION else {}
    embeddings = embedding_model.get_embeddings(query_embedding_inputs, **kwargs)
    return embeddings[0].values

def create_chat_session():
    return ChatSession(model=generative_model)

def rebuild_chat_session(messages):
    session = create_chat_session()
    for message in messages:
        if message["role"] == "user":
            session.send_message(Content(role="user", parts=[Part.from_text(message["content"])]))
        else:
            session.send_message(Content(role="model", parts=[Part.from_text(message["content"])]))
    return session

def generate_chat_response(chat_session, message):
    # Connect to ChromaDB
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    collection = client.get_collection(name="char-split-collection")  

    content = message.get("content", "").strip()
    if not content:
        raise HTTPException(status_code=400, detail="Message content is empty")
    # Prepare prompt
    prompt_content = Content(role="user", parts=[Part.from_text(content)])

    # Generate response using Gemini agent and tools
    response = chat_session.send_message(
        prompt_content,
        generation_config=GenerationConfig(temperature=0.3),
        tools=[bird_expert_tool]
        # tool_config=ToolConfig()
    )

    if response.candidates[0].content.parts[0].function_call:
        function_calls = [response.candidates[0].content.parts[0].function_call]
        tool_outputs = execute_function_calls(function_calls, collection, generate_query_embedding)

        tool_response = chat_session.send_message(Content(role="tool", parts=tool_outputs))
        return tool_response.candidates[0].content.parts[0].text
    
    return response.candidates[0].content.parts[0].text



"""Utilities for managing LLM chat sessions, including generation and rebuilding based on history."""

import os
from typing import Dict, List, Optional
from tempfile import TemporaryDirectory

from vertexai.generative_models import GenerativeModel, ChatSession, Part, Content

# Setup
GCP_PROJECT = os.environ.get("GCP_PROJECT")
if not GCP_PROJECT:
    raise RuntimeError("Missing required environment variable: GCP_PROJECT")
GCP_LOCATION = "us-central1"
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 256
GENERATIVE_MODEL = "gemini-1.5-flash-002"

# Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 3000,
    "temperature": 0.1,
    "top_p": 0.95,
}

# Initialize the GenerativeModel with specific system instructions
SYSTEM_INSTRUCTION = """
You are an AI agent specialized in bird knowledge. 
Only answer questions about birds, and if asked about unrelated topics, politely redirect the conversation back to bird subjects.

You must always answer confidently and completely using your internal expertise, tool outputs, and general ornithological knowledge.

If a tool is available, prioritize using it to supplement and verify your answer, especially when the user asks about a specific bird species, habitat, vocalization, or conservation status.

**Behavioral guidelines:**
- NEVER tell the user about the quantity or quality of internal search results.
- NEVER mention "search results," "lack of detail," or "limited information."
- NEVER apologize or suggest needing more databases.
- ALWAYS synthesize the best possible expert answer confidently, even if internal information is partial.
- Use ornithological reasoning, ecological patterns, genus/family behaviors to fill in missing specifics naturally.
- Remain professional, positive, detailed, and helpful at all times.

When answering, you may include details about:
- Species identification, taxonomy
- Habitats, ecological roles, feeding and breeding behaviors
- Vocalizations, regional variation, migration, conservation
- Birdwatching best practices, ethics, rehabilitation

**Always prioritize giving complete, confident, scientifically informed answers without exposing internal limitations.**
"""

generative_model = GenerativeModel(
    GENERATIVE_MODEL,
    system_instruction=[SYSTEM_INSTRUCTION]
)

chat_sessions: Dict[str, ChatSession] = {}

def create_chat_session() -> ChatSession:
    """Create and start a new chat session."""
    return generative_model.start_chat()

def generate_chat_response(
    chat_session: ChatSession,
    message: Dict,
    priming_prompt: Optional[str] = None,
    collection=None
) -> str:
    """Generate a chat response, optionally using a tool for bird info retrieval."""
    from api.utils.agent_tools import bird_expert_tool, execute_function_calls, generate_query_embedding

    message_parts = []

    if priming_prompt:
        message_parts.append(priming_prompt)
    if message.get("content"):
        message_parts.append(message["content"])
    if not message_parts:
        raise ValueError("Message must contain either priming text or user content")

    user_prompt_text = " ".join(message_parts)

    initial_response = chat_session.send_message(
        user_prompt_text,
        tools=[bird_expert_tool],
        generation_config=generation_config
    )

    function_calls = initial_response.candidates[0].function_calls if initial_response.candidates else []

    if function_calls and collection:
        tool_outputs = execute_function_calls(
            function_calls=function_calls,
            collection=collection,
            embed_func=generate_query_embedding
        )

        combined_parts = [
            Part.from_text(f"User question: {user_prompt_text}"),
            Part.from_text("Internal search results (may be partial):"),
            *tool_outputs,
            Part.from_text(
                "Please combine your own bird expertise with the search results "
                "to provide a complete answer."
            )
        ]

        final_response = chat_session.send_message(
            Content(role="user", parts=combined_parts),
            generation_config=generation_config
        )

        final_text = final_response.text.strip()
    else:
        final_text = initial_response.text.strip()

    fallback_phrases = [
        "not enough information", "insufficient data",
        "cannot answer", "fragmented", "unclear"
    ]
    if any(p in final_text.lower() for p in fallback_phrases):
        print("Using external info")
        fallback_info = """
        Although detailed data on this bird may not be available, most species typically exhibit
        region-specific behaviors, seasonal migration patterns, and specialized feeding habits
        adapted to their local environment.
        """
        fallback_response = chat_session.send_message(
            fallback_info,
            generation_config=generation_config
        )
        return fallback_response.text

    return final_text

def rebuild_chat_session(chat_history: List[Dict]) -> ChatSession:
    """Rebuild a chat session from a saved chat history."""
    new_session = create_chat_session()

    for message in chat_history:
        if message["role"] == "user" and message.get("content"):
            new_session.send_message(
                message["content"],
                generation_config=generation_config
            )
        elif message["role"] == "assistant" and "content" in message and "Identified:" in message["content"]:
            content = message["content"]
        elif message["role"] == "assistant" and message.get("content"):
            new_session.send_message(
                message["content"],
                generation_config=generation_config
            )

    return new_session

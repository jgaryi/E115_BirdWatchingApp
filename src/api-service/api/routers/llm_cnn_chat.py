"""FastAPI Router for Multimodal LLM Chat with External Bird Audio Identification."""

import os
import uuid
import time
import base64
from tempfile import TemporaryDirectory
from typing import Dict, Optional
import requests

from fastapi import APIRouter, Header, HTTPException

from chromadb import HttpClient

# Utilities for LLM session and response handling
from api.utils.llm_cnn_utils import (
    chat_sessions,
    create_chat_session,
    generate_chat_response,
    rebuild_chat_session
)

# Chat storage and management utility
from api.utils.chat_utils import ChatHistoryManager

CHROMADB_HOST = os.environ.get("CHROMADB_HOST", "localhost")
CHROMADB_PORT = int(os.environ.get("CHROMADB_PORT", 8000))
client = HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)

collection = client.get_collection(name="char-split-collection")

# Initialize FastAPI router
router = APIRouter()

# Initialize chat history manager and sessions
chat_manager = ChatHistoryManager(model="llm-cnn")

@router.get("/chats")
async def get_chats(x_session_id: str = Header(None, alias="X-Session-ID"), limit: Optional[int] = None):
    """Fetch recent chat history."""
    return chat_manager.get_recent_chats(x_session_id, limit)

@router.get("/chats/{chat_id}")
async def get_chat(chat_id: str, x_session_id: str = Header(None, alias="X-Session-ID")):
    """Fetch a specific chat by ID."""
    chat = chat_manager.get_chat(chat_id, x_session_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.post("/chats")
async def start_chat_with_llm(message: Dict, x_session_id: str = Header(None, alias="X-Session-ID")):
    """Start a new chat session with LLM."""
    chat_id = str(uuid.uuid4())
    current_time = int(time.time())
    chat_session = create_chat_session()
    chat_sessions[chat_id] = chat_session

    message["message_id"] = str(uuid.uuid4())
    message["role"] = "user"

    content = message.get("content", "").strip()
    user_question = content if content.lower() not in ["an audio file has been uploaded", "audio uploaded"] else ""

    filename = message.get("name", "audio.mp3")

    visible_user_message = {
        "message_id": message["message_id"],
        "role": message["role"],
        "audio": message.get("audio"),
        "name": filename,
        "content": user_question
    }

    assistant_response = ""

    if message.get("audio"):
        base64_string = message["audio"]
        base64_data = base64_string.split(",", 1)[1] if "," in base64_string else base64_string

        try:
            audio_bytes = base64.b64decode(base64_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid audio base64: {str(e)}") from e

        with TemporaryDirectory() as tmpdir:
            audio_path = os.path.join(tmpdir, "upload.mp3")
            with open(audio_path, "wb") as file_obj:
                file_obj.write(audio_bytes)

            with open(audio_path, "rb") as upload_file:
                files = {"file": ("upload.mp3", upload_file, "audio/mpeg")}
                try:
                    birdnet_response = requests.post("http://birdnet_app:9090/analyze-bird", files=files, timeout=10)
                    birdnet_response.raise_for_status()
                    birdnet_result = birdnet_response.json()
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"BirdNET error: {str(e)}") from e

            scientific_name = birdnet_result.get("scientific_name", "").strip()
            confidence = birdnet_result.get("average_confidence")

            if not scientific_name or "not identified" in scientific_name.lower():
                assistant_response = "Bird species could not be identified."
            else:
                if confidence is not None and scientific_name.lower() not in ["doliornis sclateri", "hapalopsittaca melanotis"]:
                    species_statement = f"The species identified is **{scientific_name}** ({round(confidence * 100, 1)}% confidence)."
                else:
                    species_statement = f"The species identified is **{scientific_name}**."

                if user_question:
                    full_prompt = f"{scientific_name}\n\nUser asked: {user_question}"
                    assistant_response = generate_chat_response(chat_session, {"content": full_prompt}, collection=collection)
                else:
                    _ = generate_chat_response(chat_session, {"content": scientific_name}, collection=collection)
                    assistant_response = species_statement

    elif user_question:
        full_prompt = user_question
        assistant_response = generate_chat_response(chat_session, {"content": full_prompt}, collection=collection)
    else:
        raise HTTPException(status_code=400, detail="Please provide audio or content.")

    assistant_message = {
        "message_id": str(uuid.uuid4()),
        "role": "assistant",
        "content": assistant_response
    }

    chat_response = {
        "chat_id": chat_id,
        "title": user_question[:50] + "..." if user_question else "Bird Audio Analysis",
        "dts": current_time,
        "messages": [visible_user_message, assistant_message]
    }

    chat_manager.save_chat(chat_response, x_session_id)
    return chat_response

@router.post("/chats/{chat_id}")
async def continue_chat_with_llm(chat_id: str, message: Dict, x_session_id: str = Header(None, alias="X-Session-ID")):
    """Continue an existing chat session."""
    chat = chat_manager.get_chat(chat_id, x_session_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    chat_session = chat_sessions.get(chat_id)
    if not chat_session:
        chat_session = rebuild_chat_session(chat["messages"])
        chat_sessions[chat_id] = chat_session

    current_time = int(time.time())
    chat["dts"] = current_time

    message["message_id"] = str(uuid.uuid4())
    message["role"] = "user"

    content = message.get("content", "").strip()
    user_question = content if content.lower() not in ["an audio file has been uploaded", "audio uploaded"] else ""
    filename = message.get("name", "audio.mp3")

    visible_user_message = {
        "message_id": message["message_id"],
        "role": message["role"],
        "audio": message.get("audio"),
        "name": filename,
        "content": user_question
    }

    if message.get("audio"):
        base64_string = message["audio"]
        base64_data = base64_string.split(",", 1)[1] if "," in base64_string else base64_string

        try:
            audio_bytes = base64.b64decode(base64_data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid audio base64: {str(e)}") from e

        with TemporaryDirectory() as tmpdir:
            audio_path = os.path.join(tmpdir, "upload.mp3")
            with open(audio_path, "wb") as file_obj:
                file_obj.write(audio_bytes)

            with open(audio_path, "rb") as upload_file:
                files = {"file": ("upload.mp3", upload_file, "audio/mpeg")}
                try:
                    birdnet_response = requests.post("http://birdnet_app:9090/analyze-bird", files=files, timeout=10)
                    birdnet_response.raise_for_status()
                    birdnet_result = birdnet_response.json()
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"BirdNET error: {str(e)}") from e

            scientific_name = birdnet_result.get("scientific_name", "").strip()
            confidence = birdnet_result.get("average_confidence")

            if not scientific_name or "not identified" in scientific_name.lower():
                assistant_response = "Bird species could not be identified."
            else:
                if confidence is not None and scientific_name.lower() not in ["doliornis sclateri", "hapalopsittaca melanotis"]:
                    species_statement = f"The species identified is **{scientific_name}** ({round(confidence * 100, 1)}% confidence)."
                else:
                    species_statement = f"The species identified is **{scientific_name}**."

                if user_question:
                    full_prompt = f"{scientific_name}\n\nUser asked: {user_question}"
                    assistant_response = generate_chat_response(chat_session, {"content": full_prompt}, collection=collection)
                else:
                    _ = generate_chat_response(chat_session, {"content": scientific_name}, collection=collection)
                    assistant_response = species_statement

    elif user_question:
        full_prompt = user_question
        assistant_response = generate_chat_response(chat_session, {"content": full_prompt}, collection=collection)
    else:
        raise HTTPException(status_code=400, detail="Please provide audio or content.")

    assistant_message = {
        "message_id": str(uuid.uuid4()),
        "role": "assistant",
        "content": assistant_response
    }

    chat["messages"].append(visible_user_message)
    chat["messages"].append(assistant_message)

    chat_manager.save_chat(chat, x_session_id)
    return chat

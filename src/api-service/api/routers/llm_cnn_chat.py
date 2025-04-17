
from fastapi import APIRouter, Header, Form, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from typing import Optional
import uuid
import time
import base64
import os
from pathlib import Path
import mimetypes
from api.utils.llm_cnn_utils import (
    chat_sessions,
    create_chat_session,
    generate_chat_response1,
    rebuild_chat_session1
)
from api.utils.chat_utils import ChatHistoryManager

router = APIRouter()
chat_manager = ChatHistoryManager(model="llm-cnn")

# GET endpoint to fetch recent chats
@router.get("/chats")
async def get_chats(x_session_id: str = Header(None, alias="X-Session-ID"), limit: Optional[int] = None):
    print("x_session_id:", x_session_id)
    return chat_manager.get_recent_chats(x_session_id, limit)

# GET endpoint to fetch a specific chat by its ID
@router.get("/chats/{chat_id}")
async def get_chat(chat_id: str, x_session_id: str = Header(None, alias="X-Session-ID")):
    print("x_session_id:", x_session_id)
    chat = chat_manager.get_chat(chat_id, x_session_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

# POST endpoint for starting a new chat
@router.post("/chats")
async def start_chat_with_llm(
    content: str = Form(""),
    file: Optional[UploadFile] = File(None),
    x_session_id: str = Header(None, alias="X-Session-ID")
):
    chat_id = str(uuid.uuid4())
    current_time = int(time.time())
    chat_session = create_chat_session()
    chat_sessions[chat_id] = chat_session

    message = {
        "message_id": str(uuid.uuid4()),
        "role": "user",
        "content": content.strip(),
    }

    if file:
        audio_bytes = await file.read()
        base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
        message["audio"] = base64_audio

    assistant_response = generate_chat_response1(chat_session, message)

    title = message["content"] or "Audio chat"
    if len(title) > 50:
        title = title[:50] + "..."

    chat_response = {
        "chat_id": chat_id,
        "title": title,
        "dts": current_time,
        "messages": [
            message,
            {
                "message_id": str(uuid.uuid4()),
                "role": "assistant",
                "content": assistant_response
            }
        ]
    }

    chat_manager.save_chat(chat_response, x_session_id)
    return chat_response

# POST endpoint for continuing an existing chat
@router.post("/chats/{chat_id}")
async def continue_chat_with_llm(
    chat_id: str,
    content: str = Form(""),
    file: Optional[UploadFile] = File(None),
    x_session_id: str = Header(None, alias="X-Session-ID")
):
    chat = chat_manager.get_chat(chat_id, x_session_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    chat_session = chat_sessions.get(chat_id)
    if not chat_session:
        chat_session = rebuild_chat_session1(chat["messages"])
        chat_sessions[chat_id] = chat_session

    current_time = int(time.time())
    chat["dts"] = current_time

    message = {
        "message_id": str(uuid.uuid4()),
        "role": "user",
        "content": content.strip(),
    }

    if file:
        audio_bytes = await file.read()
        base64_audio = base64.b64encode(audio_bytes).decode("utf-8")
        message["audio"] = base64_audio

    assistant_response = generate_chat_response1(chat_session, message)

    chat["messages"].append(message)
    chat["messages"].append({
        "message_id": str(uuid.uuid4()),
        "role": "assistant",
        "content": assistant_response
    })

    chat_manager.save_chat(chat, x_session_id)
    return chat

# GET endpoint for serving audio files associated with chats
@router.get("/audio/{chat_id}/{message_id}.mp3")
async def get_chat_audio(chat_id: str, message_id: str):
    try:
        audio_path = Path(chat_manager.audio_dir) / chat_id / f"{message_id}.mp3"
        audio_path = audio_path.resolve()
        audio_dir = Path(chat_manager.audio_dir).resolve()

        if not str(audio_path).startswith(str(audio_dir)):
            raise HTTPException(status_code=403, detail="Access denied")

        if not audio_path.exists():
            raise HTTPException(status_code=404, detail="Audio not found")

        content_type, _ = mimetypes.guess_type(str(audio_path))
        return FileResponse(
            path=audio_path,
            media_type=content_type or "application/octet-stream"
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error serving audio: {str(e)}")

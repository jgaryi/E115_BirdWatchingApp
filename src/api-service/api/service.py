from fastapi import FastAPI
from fastapi.routing import APIRouter
from starlette.middleware.cors import CORSMiddleware
from api.routers import llm_cnn_chat, bird_map, bird_sound

app = FastAPI(title="API Server", description="API Server", version="v1")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API under /api
api_router = APIRouter()
api_router.include_router(bird_map.router, prefix="/bird_maps")
api_router.include_router(bird_sound.router, prefix="/bird_sounds")
api_router.include_router(llm_cnn_chat.router, prefix="/llm-cnn")

app.include_router(api_router, prefix="/api")

@app.get("/")
async def get_index():
    return {"message": "Welcome to the Bird Watching App"}

import logging
for route in app.routes:
    logging.warning(f"Registered route: {route.path} [{route.methods}]")
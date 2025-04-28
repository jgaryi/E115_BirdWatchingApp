'''Routes for the Bird Watching App.'''

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.routers import llm_cnn_chat
from api.routers import bird_map, bird_sound

# Setup FastAPI app
app = FastAPI(title="API Server", description="API Server", version="v1")

# Enable CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
@app.get("/")
async def get_index():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to the Bird Watching App"}

# Additional routers here
app.include_router(bird_map.router, prefix="/bird_maps")
app.include_router(bird_sound.router, prefix="/bird_sounds")
app.include_router(llm_cnn_chat.router, prefix="/llm-cnn")

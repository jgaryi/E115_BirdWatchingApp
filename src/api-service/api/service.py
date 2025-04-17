from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.routers import llm_cnn_chat
from api.routers import newsletter, podcast

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
    return {"message": "Welcome to AC215"}

# Additional routers here
app.include_router(newsletter.router, prefix="/newsletters")
app.include_router(podcast.router, prefix="/podcasts")
app.include_router(llm_cnn_chat.router, prefix="/llm-cnn")


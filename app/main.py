from fastapi import FastAPI
from app.router import router as moderate_router


app = FastAPI(
    title="NSFW Content Detector API",
    description="API для проверки изображений на наличие NSFW контента с помощью DeepAI."
)


app.include_router(moderate_router)
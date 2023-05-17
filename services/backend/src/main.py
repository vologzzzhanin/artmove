from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from tortoise import Tortoise

from src.database.config import TORTOISE_ORM
from src.database.register import register_tortoise
from .config import settings


Tortoise.init_models(["src.database.models"], "models")

from src.routes import animations, images, users

app = FastAPI(
    title="НЕДЖИПИТИ",
    description="Просто небольшая апишечка",
    version="0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(animations.router)
app.include_router(images.router)

app.mount(
    settings.upload_root,
    StaticFiles(directory=settings.upload_root),
    name="static",
)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)


@app.get("/", tags=["Health check"])
def home():
    return "Hello, World!"

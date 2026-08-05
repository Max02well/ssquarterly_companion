from fastapi import FastAPI,Path
from src.api.database.base import Base
from src.api.database.database import engine
from sqlalchemy import text
from src.api.routes import (
    # auth,
    users,
    # lessons,
    # chat,
    # search,
    # audio,
    health,
)

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print("Database connected successfully!")
    
# Base.metadata.create_all(bind=engine)  # Create tables if they don't exist

app = FastAPI(
    title="Quarterly Companion API - Authored by Maxwell Gogo",
    version="1.0.0",
    description=(
        "RAG-powered Sabbath School study "
        "and devotional audio API."
    ),
)


app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["Health Check"]
)

app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["Users"],
)

    # app.include_router(
    #     auth.router,
    #     prefix="/api/v1/auth",
    #     tags=["Authentication"],
    # )

 

# app.include_router(
#     lessons.router,
#     prefix="/api/v1/lessons",
#     tags=["Lessons"],
# )

# app.include_router(
#     chat.router,
#     prefix="/api/v1/chat",
#     tags=["Chat"],
# )

# app.include_router(
#     search.router,
#     prefix="/api/v1/search",
#     tags=["Search"],
# )

# app.include_router(
#     audio.router,
#     prefix="/api/v1/audio",
#     tags=["Audio"],
# )


@app.get("/")
async def root():
    return {
        "name": "Quarterly Companion API",
        "version": "1.0.0",
        "status": "running",
    }
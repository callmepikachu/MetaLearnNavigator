from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from database.database import init_db
from routers import learning_flow, cognitive_map, knowledge_cards, api_integration


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化数据库
    await init_db()
    print("Database initialized successfully")
    yield
    # 关闭时的清理工作
    print("Application shutting down")


app = FastAPI(
    title="MetaLearnNavigator API",
    description="元认知学习导航器后端API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 路由注册
app.include_router(learning_flow.router, prefix="/api/learning-flow", tags=["learning-flow"])
app.include_router(cognitive_map.router, prefix="/api/cognitive-map", tags=["cognitive-map"])
app.include_router(knowledge_cards.router, prefix="/api/knowledge-cards", tags=["knowledge-cards"])
app.include_router(api_integration.router, prefix="/api/external", tags=["external-api"])


@app.get("/")
async def root():
    return {"message": "MetaLearnNavigator API is running"}


@app.get("/health")
async def health_check():
    return {"status": "OK", "message": "Service is healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

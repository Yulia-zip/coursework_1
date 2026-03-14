
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.api.compare import router as compare_router

# Получаем путь к папке fronted
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTED_DIR = os.path.join(BASE_DIR, "fronted")

app = FastAPI(
    title="ISEM Code Comparison API",
    description="API для сравнения Python кода",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение статических файлов из папки fronted
app.mount("/static", StaticFiles(directory=FRONTED_DIR), name="static")

# Подключение роутеров API
app.include_router(compare_router)

@app.get("/")
async def serve_index():
    """Главная страница - отдаем index.html"""
    return FileResponse(os.path.join(FRONTED_DIR, "index.html"))

@app.get("/api")
async def api_info():
    """Информация о API"""
    return {
        "message": "ISEM Code Comparison API",
        "version": "1.0.0",
        "endpoints": {
            "compare": "/compare/",
            "health": "/compare/health",
            "docs": "/docs"
        }
    }
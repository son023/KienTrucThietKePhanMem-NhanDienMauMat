"""
Ứng dụng chính cho hệ thống kiểm tra an ninh bằng đồng tử mắt
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from controller.EyeRecognitionModelController import router as eye_recognition_model_router

app = FastAPI(
    title="Hệ thống Kiểm tra An ninh bằng Đồng tử Mắt",
    description="API cho hệ thống kiểm tra an ninh bằng đồng tử mắt",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

uploads_dir = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

app.include_router(eye_recognition_model_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0",
        port=8000,
        reload=True
    )
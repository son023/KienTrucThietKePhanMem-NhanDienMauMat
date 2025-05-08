"""
Ứng dụng chính cho hệ thống kiểm tra an ninh bằng đồng tử mắt - Phát hiện vùng mắt
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from controller.EyeDetectionModelController import router as eye_detection_model_router

# Tạo ứng dụng FastAPI
app = FastAPI(
    title="Hệ thống Kiểm tra An ninh bằng Đồng tử Mắt - Phát hiện vùng mắt",
    description="API cho hệ thống phát hiện vùng mắt trong ảnh",
    version="1.0.0",
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
uploads_dir = os.getenv("UPLOAD_DIR", "./uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

app.include_router(eye_detection_model_router)

@app.get("/")
async def root():
    """
    Root endpoint để kiểm tra API hoạt động
    """
    return {"message": "Chào mừng đến với API Hệ thống Kiểm tra An ninh bằng Đồng tử Mắt - Phát hiện vùng mắt"}

# Khởi động ứng dụng với uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0",
        port=8001,  # Sử dụng cổng khác để tránh xung đột với service nhận diện màu mắt
        reload=True
    )
# controller/EyeDetectionModelController.py
from fastapi import APIRouter, HTTPException, File, UploadFile, Form, status, Query
from typing import List, Optional
import os
import uuid
import shutil

from entity.EyeDetectionModel import EyeDetectionModel
from dao.EyeDetectionModelDAO import EyeDetectionModelDAO

router = APIRouter(
    prefix="/api/eye-detection-model",
    tags=["eye-detection-model"]
)

eye_detection_model_dao = EyeDetectionModelDAO()

@router.get("", response_model=List[EyeDetectionModel])
async def get_all_eye_detection_model(
    active_only: bool = Query(True, description="Chỉ lấy mô hình đang hoạt động")
):
    try:
        items = eye_detection_model_dao.get_all(active_only)
        return items
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi lấy danh sách mô hình phát hiện mắt: {str(e)}"
        )

@router.get("/{model_id}", response_model=EyeDetectionModel)
async def get_eye_detection_model_by_id(model_id: int):
    try:
        item = eye_detection_model_dao.get_by_id(model_id)
        
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy mô hình phát hiện mắt với ID {model_id}"
            )
            
        return item
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi lấy thông tin mô hình phát hiện mắt: {str(e)}"
        )
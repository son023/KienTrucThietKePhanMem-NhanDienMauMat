from fastapi import APIRouter, HTTPException, File, UploadFile, Form, status, Query, Body, Depends
from typing import List, Optional
import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.models as models
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import cv2
import numpy as np
from datetime import datetime

import time
from torchvision.models.resnet import ResNet50_Weights
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


from entity.EyeRecognitionModel import EyeRecognitionModel
from entity.EyeRecognitionSampleHistory import EyeRecognitionSampleHistory
from dao.EyeRecognitionModelDAO import EyeRecognitionModelDAO
from dao.EyeRecognitionSampleDAO import EyeRecognitionSampleDAO
from dao.EyeRecognitionSampleHistoryDAO import EyeRecognitionSampleHistoryDAO


router = APIRouter(
    prefix="/api/eye-recognition-model",
    tags=["eye-recognition-model"]
)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

@router.get("", response_model=List[EyeRecognitionModel])
async def get_all_models(
    active_only: bool = Query(True, description="Chỉ lấy các mô hình đang hoạt động")
):
    try:
        models = await EyeRecognitionModelDAO.get_all(active_only)
        return models
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi lấy danh sách mô hình nhận dạng mắt: {str(e)}"
        )

@router.get("/{model_id}", response_model=EyeRecognitionModel)
async def get_model_by_id(model_id: int):
    try:
        model = await EyeRecognitionModelDAO.get_by_id(model_id)
        
        if not model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy mô hình nhận dạng mắt với ID {model_id}"
            )
        
        return model
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi lấy thông tin mô hình nhận dạng mắt: {str(e)}"
        )

@router.post("", response_model=EyeRecognitionModel)
async def create_model(
    model_link: str = Body(...),
    eye_model_name: str = Body(...),
    history_ids: List[int] = Body(...),
    accuracy: Optional[float] = Body(None),
    is_active: bool = Body(True),
    epochs: Optional[int] = Body(None),
    learning_rate: Optional[float] = Body(None),
    image_size: Optional[int] = Body(None),
    batch_size: Optional[int] = Body(None),
    mapping_label: Optional[str] = Body(None)
):
    try:
        # Kiểm tra các lịch sử mẫu tồn tại
        histories = []
        for history_id in history_ids:
            history = await EyeRecognitionSampleHistoryDAO.get_by_id(history_id)
            if not history:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Không tìm thấy lịch sử mẫu nhận dạng mắt với ID {history_id}"
                )
            histories.append(history)
        
        # Tạo đối tượng mô hình mới
        new_model = EyeRecognitionModel(
            id=0,
            modelLink=model_link,
            eyeModelName=eye_model_name,
            eyeRecognitionSampleTrain=histories,
            accuracy=accuracy,
            isActive=is_active,
            epochs=epochs,
            learningRate=learning_rate,
            imageSize=image_size,
            batchSize=batch_size,
            mappingLabel=mapping_label,
            createDate=datetime.now()
        )
        
        # Lưu vào cơ sở dữ liệu
        saved_model = await EyeRecognitionModelDAO.create(new_model)
        
        return saved_model
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi tạo mô hình nhận dạng mắt: {str(e)}"
        )
        
@router.post("/is-members-has-enough-samples", response_model= List[int])
async def check_members_has_enough_samples( memberIds: List[int] = Body(...)):
    try:
        memberIds_result = []
        for member_id in memberIds:
            is_enough = await EyeRecognitionSampleDAO.is_member_has_enough_samples(member_id)
            if is_enough:
                memberIds_result.append(member_id)
        return memberIds_result
    except Exception as e:
        raise HTTPException (status_code=500, detail="Lỗi ở check_members_has_enough_samples")

@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_model(model_id: int):
    """
    Xóa mô hình nhận dạng mắt
    """
    try:
        # Kiểm tra mô hình tồn tại
        existing_model = await EyeRecognitionModelDAO.get_by_id(model_id)
        if not existing_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy mô hình nhận dạng mắt với ID {model_id}"
            )
        
        # Xóa khỏi cơ sở dữ liệu
        await EyeRecognitionModelDAO.delete(model_id)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi xóa mô hình nhận dạng mắt: {str(e)}"
        )

@router.get("/get-history-by-model-id/{model_id}", response_model=List[EyeRecognitionSampleHistory])
async def get_all_histories_by_model_id(model_id: int):
    try:
        histories = await EyeRecognitionSampleHistoryDAO.get_all_by_model_id(model_id)
        return histories
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi lấy danh sách lịch sử mẫu nhận dạng mắt: {str(e)}"
        )


@router.post("/train", response_model=EyeRecognitionModel)
async def train_model(
    memberIds: List[int] = Body(...),
    model_name: str = Body(...),
    epochs: Optional[int] = Body(...),
    batch_size: Optional[int] = Body(...),
    learning_rate: Optional[float] = Body(...),
    image_size: Optional[int] = Body(...),
):
    try:
        eye_recognition_samples = []
        image_paths = []
        labels = []
        for memberId in memberIds:
            eye_recognition_sample = EyeRecognitionSampleDAO.get_by_member_id(memberId)
            eye_recognition_samples.extend(eye_recognition_sample)
        for sample in eye_recognition_samples:
            image_paths.append(sample.eyeImageLink)
            labels.append(sample.label)
      
        iris_model = EyeRecognitionModel()
        iris_model.eyeModelName = model_name
        iris_model.eyeRecognitionSampleTrain = []
        iris_model.createDate = datetime.now()
        iris_model.epochs = epochs
        iris_model.batchSize = batch_size
        iris_model.learningRate = learning_rate
        iris_model.imageSize = image_size
        
        train_transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((iris_model.imageSize, iris_model.imageSize)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(10),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        val_transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((iris_model.imageSize, iris_model.imageSize)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        
        train_paths, temp_paths, train_labels, temp_labels = train_test_split(
            image_paths, labels, test_size=0.3, stratify=labels, random_state=42
        )
        
        val_paths, test_paths, val_labels, test_labels = train_test_split(
            temp_paths, temp_labels, test_size=0.5, stratify=temp_labels, random_state=42
        )
        
        print(f"Train samples: {len(train_paths)}")
        print(f"Validation samples: {len(val_paths)}")
        print(f"Test samples: {len(test_paths)}")
        
        
        train_dataset = IrisDataset(train_paths, train_labels, transform=train_transform)
        val_dataset = IrisDataset(val_paths, val_labels, transform=val_transform)
        test_dataset = IrisDataset(test_paths, test_labels, transform=val_transform)
        
        train_loader = DataLoader(train_dataset, batch_size=iris_model.batchSize, shuffle=True, num_workers=0)
        val_loader = DataLoader(val_dataset, batch_size=iris_model.batchSize, shuffle=False, num_workers=0)
        test_loader = DataLoader(test_dataset, batch_size=iris_model.batchSize, shuffle=False, num_workers=0)
        
        num_classes = len(set(labels))
        print(num_classes)
        model = load_model(num_classes)
        
        print("Bắt đầu huấn luyện mô hình...")
        model, val_accuracy, training_time = train_model1(
            model, train_loader, val_loader, 
            iris_model.epochs, iris_model.learningRate
        )
        
        iris_model.accuracy = val_accuracy / 100.0  
        iris_model.trainingTime = int(training_time)
        
        model_path = f"models/{iris_model.eyeModelName}.pt"
        torch.save(model.state_dict(), model_path)
        iris_model.modelLink = model_path

        iris_model.mappingLabel = " ".join(map(str, {idx: label for label, idx in train_dataset.label_to_idx.items()}))
        
        for eye_recognition_sample in eye_recognition_samples:
            history = EyeRecognitionSampleHistory(id = 0, eyeRecognitionSample= eye_recognition_sample, notes= model_name)
            iris_model.eyeRecognitionSampleTrain.append(history)
            
        model_result = await EyeRecognitionModelDAO.create(iris_model)
        
        return model_result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi tạo model: {str(e)}"
        )
        
def train_model1( model, train_loader, val_loader, num_epochs, learning_rate, patience=5):
    """
    Huấn luyện mô hình với early stopping
    """
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=learning_rate)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=2)
    
    best_val_loss = float('inf')
    epochs_no_improve = 0
    best_model_path = "models/best_iris_classifier.pt"
    
    training_start_time = time.time()
    
    for epoch in range(num_epochs):
        start_time = time.time()
        
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        
        train_loss = running_loss / len(train_loader)
        train_acc = 100 * correct / total
        
        model.eval()
        val_correct = 0
        val_total = 0
        val_loss = 0.0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()
        
        val_loss = val_loss / len(val_loader)
        val_acc = 100 * val_correct / val_total
        
        end_time = time.time()
        epoch_time = end_time - start_time
        
        print(f"Epoch [{epoch+1}/{num_epochs}] Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%, "
                f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%, Time: {epoch_time:.2f}s")
        
        # Early stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            epochs_no_improve = 0
            torch.save(model.state_dict(), best_model_path)
            print(f"Saved best model with Val Loss: {best_val_loss:.4f}")
        else:
            epochs_no_improve += 1
            print(f"No improvement in {epochs_no_improve}/{patience} epochs.")
            if epochs_no_improve >= patience:
                print("Early stopping triggered.")
                break
        
        # Cập nhật learning rate
        scheduler.step(val_loss)
    
    # Tính tổng thời gian huấn luyện
    training_time = time.time() - training_start_time
    print(f"Tổng thời gian huấn luyện: {training_time:.2f}s")
    
    # Tải mô hình tốt nhất
    if os.path.exists(best_model_path):
        model.load_state_dict(torch.load(best_model_path))
    
    return model, val_acc, training_time


def load_model( num_classes):
        """
        Tải và điều chỉnh mô hình ResNet-50
        """
        model = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
        for param in model.parameters():
            param.requires_grad = False
        
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, num_classes)
        for param in model.fc.parameters():
            param.requires_grad = True
        
        model.to(device)
        return model
    
class IrisDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
        self.label_to_idx = {label: idx for idx, label in enumerate(sorted(set(labels)))}

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        label = self.labels[idx]
        
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Không thể đọc ảnh {img_path}")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        if self.transform:
            img = self.transform(img)
        label_idx = self.label_to_idx[label]
        return img, label_idx 
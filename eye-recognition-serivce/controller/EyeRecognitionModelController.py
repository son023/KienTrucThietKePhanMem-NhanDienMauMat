from fastapi import APIRouter, HTTPException, status, Body
import os
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.models as models
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import cv2
from datetime import datetime

import uuid
import time
from torchvision.models.resnet import ResNet50_Weights
from sklearn.metrics import precision_score, f1_score


from model.EyeRecognitionModel import EyeRecognitionModel
from model.EyeRecognitionSample import EyeRecognitionSample
from model.EyeRecognitionSampleHistory import EyeRecognitionSampleHistory
from utils.image_downloader import ImageDownloader


router = APIRouter(
    prefix="/api/eye-recognition-model",
    tags=["eye-recognition-model"]
)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


@router.post("/train", response_model = EyeRecognitionModel)
async def train_model(request_data: dict = Body(...)):
    try:
        print("=== TRAIN MODEL START ===")
        print(f"Request data keys: {request_data.keys()}")
        
        # Extract parameters từ request
        samples_data = request_data.get("samples", [])
        modelName = request_data.get("modelName", "")
        epochs = request_data.get("epochs", 20)
        batchSize = request_data.get("batchSize", 32)
        learningRate = request_data.get("learningRate", 0.001)
        imageSize = request_data.get("imageSize", 224)
        
        print(f"Parameters extracted - Model: {modelName}, Samples: {len(samples_data)}")
        
        # Convert dict samples thành EyeRecognitionSample objects
        samples = []
        print("Starting sample conversion...")
        
        for i, sample_data in enumerate(samples_data):
            try:
                if i % 50 == 0:  # Log every 50 samples
                    print(f"Processing sample {i}/{len(samples_data)}")
                
                # Simple conversion - skip complex nested objects for now
                sample_simple = {
                    "id": sample_data.get("id"),
                    "eyeImageLink": sample_data.get("eyeImageLink"),
                    "label": sample_data.get("label"),
                    "isActive": sample_data.get("isActive", True),
                    "captureDate": sample_data.get("captureDate"),
                    "member": None  # Tạm thời skip member object để test
                }
                
                sample = EyeRecognitionSample(**sample_simple)
                samples.append(sample)
                
            except Exception as e:
                print(f"ERROR processing sample {i}: {e}")
                print(f"Sample data: {sample_data}")
                raise e
        
        print(f"Sample conversion completed: {len(samples)} samples")
        
        # Khởi tạo ImageDownloader
        print("Initializing ImageDownloader...")
        image_downloader = ImageDownloader()
        
        # Lấy image URLs từ samples
        image_urls = [sample.eyeImageLink for sample in samples]
        labels = [sample.label for sample in samples]
        
        print(f"Starting image download and organization: {len(image_urls)} images")
        # Tải ảnh và organize theo labels
        organized_images = image_downloader.download_and_organize_by_labels(image_urls, labels)
        print(f"Image organization completed: {len(organized_images)} labels")
        
        # Convert organized dict thành flat lists cho training
        all_image_paths = []
        all_labels = []
        for label, paths in organized_images.items():
            all_image_paths.extend(paths)
            all_labels.extend([label] * len(paths))
        
        print(f"Prepared for training: {len(all_image_paths)} images, {len(set(all_labels))} unique labels")
        
        # Rest of the training code...
        print("Creating model object...")
        iris_model = EyeRecognitionModel()
        iris_model.eyeModelName = modelName
        iris_model.createDate = datetime.now()
        iris_model.epochs = epochs
        iris_model.batchSize = batchSize
        iris_model.learningRate = learningRate
        iris_model.imageSize = imageSize
        
        train_transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((iris_model.imageSize, iris_model.imageSize)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(10),

            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        val_transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((iris_model.imageSize, iris_model.imageSize)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        
        train_paths, val_paths, train_labels, val_labels = train_test_split(
            all_image_paths, all_labels, test_size=0.2, stratify= all_labels, random_state=42
        )
        
        print(f"Train: {len(train_paths)}")
        print(f"Val: {len(val_paths)}")
        
        train_dataset = IrisDataSet(train_paths, train_labels, train_transform)
        val_dataset = IrisDataSet(val_paths, val_labels, val_transform )
        
        train_loader = DataLoader(train_dataset, batch_size= iris_model.batchSize, shuffle = True, num_workers=0)
        val_loader = DataLoader(val_dataset, batch_size = iris_model.batchSize, shuffle = True, num_workers = 0 )

        num_classes = len(set(all_labels))
        
        model = models.resnet50(weights = ResNet50_Weights.IMAGENET1K_V1)
        for param in model.parameters():
            param.requires_grad = False
            
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, num_classes)
        
        for param in model.fc.parameters():
            param.requires_grad = True
            
        model.to(device)
        
        print("Bat dau huan luyen mo hinh")
        model, val_accuracy, training_time, f1_score, precision = train_model_process(
            model, train_loader, val_loader, iris_model.epochs, iris_model.learningRate
        )
        
        iris_model.accuracy = val_accuracy
        iris_model.trainingTime = training_time
        iris_model.f1Score = f1_score
        iris_model.precision = precision
        
        iris_model.mappingLabel = " ".join(map(str, {idx:label for label, idx in train_dataset.label_to_idx.items()}))
        
        # Lưu model file với UUID
        print("Saving model file...")
        os.makedirs("models", exist_ok=True)  # Tạo thư mục nếu chưa có
        model_id = str(uuid.uuid4())
        final_model_path = f"models/{model_id}.pt"
        torch.save(model.state_dict(), final_model_path)
        iris_model.modelLink = model_id  # Chỉ lưu UUID
        print(f"Model file saved: {final_model_path}")
        
        # Tạo histories từ samples đã train
        print("Creating training history records...")
        histories = []
        for sample in samples:
            history = EyeRecognitionSampleHistory(
                eyeRecognitionSample=sample,
                notes=f"Trained with model {modelName} - Label: {sample.label}"
            )
            histories.append(history)
        
        iris_model.eyeRecognitionSampleHistory = histories
        print(f"Created {len(histories)} history records")
        
        # Set model ID 
        iris_model.id = model_id
        
        # Cleanup temp files
        image_downloader.cleanup_temp_files(all_image_paths)
        print("Đã xóa các file ảnh tạm thời")
        
        print("Training completed successfully! Ready for user confirmation.")
        return iris_model  # Return model cho frontend để user confirm
    
    except Exception as e:
        print(f"=== TRAIN MODEL ERROR ===")
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Training error: {e}"
        )
 
def train_model_process( model, train_loader, val_loader, epochs, learning_rate):
    criterion =  nn.CrossEntropyLoss() 
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr = learning_rate)
    
    best_model_path = "models/best_iris_classifier.pt"
    best_val_loss = float('inf')
    
    training_start_time = time.time()
    
    best_val_acc = 0.0
    best_f1_score = 0.0
    best_precision = 0.0
    
    for epoch in range(epochs):
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
        train_acc = 100 * correct /total
        
        model.eval()
        val_correct = 0
        val_total = 0
        val_loss = 0.0
        
        all_predictions = []
        all_labels = []
        
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs  = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                val_total += labels.size(0)
                val_correct += (predicted == labels).sum().item()
                
                all_predictions.extend(predicted.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
        
        val_loss = val_loss / len(val_loader)
        val_acc = 100 * val_correct / val_total
        
        f1 = f1_score(all_labels, all_predictions, average='weighted')
        precision = precision_score(all_labels, all_predictions, average='weighted', zero_division=0)
        
        end_time = time.time()
        epoch_time = end_time - start_time
        
        print(f"Epoch [{epoch+1}/{epochs}] Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%, "
              f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.2f}%, "
              f"F1: {f1:.4f}, Precision: {precision:.4f}, "
              f"Time: {epoch_time:.2f}s")
         
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_val_acc = val_acc
            best_f1_score = f1
            best_precision = precision
            torch.save(model.state_dict(), best_model_path)
            print(f"Luu mo hinh tot nhat voi Val loss:{ best_val_loss:.4f}")
        
    training_time = time.time() - training_start_time
    print(f"Tong thoi gian huan luyen:{training_time:.2f}s") 
    
    if os.path.exists(best_model_path):
        model.load_state_dict(torch.load(best_model_path))
        os.remove(best_model_path)
    return model, val_acc, int(training_time), best_f1_score, best_precision            
        

class IrisDataSet(Dataset):
    def __init__(self, image_paths, labels, transform = None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform
        self.label_to_idx = { label:idx for idx, label in enumerate(sorted(set(labels)))}
        
    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_path = self.image_paths[idx]
        label = self.labels[idx]
        
        img = cv2.imread(image_path)
        
        if img is None:
            raise ValueError(f"Khong the doc anh {image_path}")
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        if self.transform:
            img = self.transform(img)
        label_idx = self.label_to_idx[label]
        
        return img, label_idx
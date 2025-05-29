import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.models as models
from .base_strategy import BaseTrainingStrategy

class VGG16Strategy(BaseTrainingStrategy):
    """VGG16 Strategy - All in one class"""
    
    def create_model(self, num_classes: int) -> nn.Module:
        model = models.vgg16(weights=models.VGG16_Weights.IMAGENET1K_V1)
        
        for param in model.features.parameters():
            param.requires_grad = False

        model.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(),
            nn.BatchNorm1d(4096),
            nn.Dropout(0.5),
            nn.Linear(4096, 1024),
            nn.ReLU(),
            nn.BatchNorm1d(1024),
            nn.Dropout(0.3),
            nn.Linear(1024, num_classes)
        )
        
        for m in model.classifier.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_normal_(m.weight)
                nn.init.constant_(m.bias, 0)
        
        return model
    
    def get_transforms(self, image_size: int):
        train_transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((256, 256)),
            transforms.RandomCrop(224),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            transforms.RandomErasing(p=0.1)
        ])
        
        val_transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        return train_transform, val_transform
    
    def get_optimizer_and_criterion(self, model: nn.Module, learning_rate: float):
        criterion = nn.CrossEntropyLoss(label_smoothing=0.1)
        optimizer = optim.AdamW(
            model.classifier.parameters(),
            lr=learning_rate * 2,
            weight_decay=0.01
        )
        return optimizer, criterion
    
    def get_strategy_name(self) -> str:
        return "VGG16" 

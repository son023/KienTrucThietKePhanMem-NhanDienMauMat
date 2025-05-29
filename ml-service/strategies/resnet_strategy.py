import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.models as models
import torchvision.transforms as transforms
from torchvision.models.resnet import ResNet50_Weights
from .base_strategy import BaseTrainingStrategy

class ResNetStrategy(BaseTrainingStrategy):
    """Strategy sử dụng ResNet50 với Transfer Learning"""
    
    def create_model(self, num_classes: int) -> nn.Module:
        model = models.resnet50(weights=ResNet50_Weights.IMAGENET1K_V1)
        
        for param in model.parameters():
            param.requires_grad = False

        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, num_classes)

        for param in model.fc.parameters():
            param.requires_grad = True
            
        return model
    
    def get_transforms(self, image_size: int):
        train_transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((image_size, image_size)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(10),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        val_transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        return train_transform, val_transform
    
    def get_optimizer_and_criterion(self, model: nn.Module, learning_rate: float):
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=learning_rate)
        return optimizer, criterion
    
    def get_strategy_name(self) -> str:
        return "ResNet50" 
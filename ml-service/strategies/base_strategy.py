from abc import ABC, abstractmethod
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from typing import Tuple

class BaseTrainingStrategy(ABC):
    """Base class cho các training strategy"""
    
    @abstractmethod
    def create_model(self, num_classes: int) -> nn.Module:
        """Tạo mô hình cho strategy này"""
        pass
    
    @abstractmethod
    def get_transforms(self, image_size: int) -> Tuple:
        """Trả về train_transform và val_transform"""
        pass
    
    @abstractmethod
    def get_optimizer_and_criterion(self, model: nn.Module, learning_rate: float) -> Tuple:
        """Trả về optimizer và criterion"""
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """Tên của strategy"""
        pass 
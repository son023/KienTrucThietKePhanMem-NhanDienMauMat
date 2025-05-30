import requests
import cv2
import numpy as np
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
import threading

class ImageDownloader:
    """
    Lớp đơn giản để tải ảnh từ URL và tổ chức theo nhãn.
    """
    def __init__(self, temp_dir="temp_images"):
        """Khởi tạo với thư mục tạm."""
        self.temp_dir = temp_dir
        os.makedirs(temp_dir, exist_ok=True)
        self.session = requests.Session()
        self.lock = threading.Lock()
    
    def download_single_image(self, url_label):
        """Tải một ảnh với URL và nhãn."""
        url, label = url_label
        
      
        label_dir = os.path.join(self.temp_dir, str(label))
        with self.lock:
            os.makedirs(label_dir, exist_ok=True)
        
        try:
            filename = f"{uuid.uuid4()}.jpg"
            if '.' in url.split('/')[-1]:
                ext = url.split('/')[-1].split('.')[-1]
                if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                    filename = f"{uuid.uuid4()}.{ext}"
            
            local_path = os.path.join(label_dir, filename)
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            return (label, local_path, True)
            
        except Exception as e:
            print(f"Lỗi tải {url}: {str(e)[:100]}")
            return (label, None, False)
    
    def download_and_organize_by_labels(self, image_urls, labels):
        """Tải ảnh song song và tổ chức theo nhãn."""
        if len(image_urls) != len(labels):
            raise ValueError("Số lượng URL phải bằng số lượng nhãn")
        
        print(f"Đang tải {len(image_urls)} ảnh...")
        organized_paths = {}
        
        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(self.download_single_image, zip(image_urls, labels)))
            
            for label, path, success in results:
                if success and path:
                    if label not in organized_paths:
                        organized_paths[label] = []
                    organized_paths[label].append(path)
        
        for label, paths in organized_paths.items():
            print(f"Nhãn {label}: {len(paths)} ảnh")
        
        valid_labels = {label: paths for label, paths in organized_paths.items() if len(paths) >= 3}
        
        if len(valid_labels) < 2:
            raise ValueError(f"Cần ít nhất 2 nhãn với 3+ ảnh mỗi nhãn. Hiện có: {len(valid_labels)}")
            
        return valid_labels
    
    def cleanup_temp_files(self, file_paths=None):
        """Xóa các file tạm."""
        if file_paths:
            for file_path in file_paths:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f"Không thể xóa file {file_path}: {e}")
        else:
            import shutil
            try:
                if os.path.exists(self.temp_dir):
                    shutil.rmtree(self.temp_dir)
                    print(f"Đã xóa thư mục tạm: {self.temp_dir}")
            except Exception as e:
                print(f"Không thể xóa thư mục {self.temp_dir}: {e}")
    
    def load_image_as_array(self, image_path):
        """Tải ảnh thành mảng numpy."""
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Không thể đọc ảnh từ {image_path}")
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
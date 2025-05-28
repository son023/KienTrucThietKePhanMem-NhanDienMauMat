import requests
import cv2
import numpy as np
from typing import List, Dict
import os
import uuid
from urllib.parse import urlparse
import time
from concurrent.futures import ThreadPoolExecutor
import threading

class ImageDownloader:
    def __init__(self, temp_dir="temp_images"):
        self.temp_dir = temp_dir
        os.makedirs(temp_dir, exist_ok=True)
        self.session = requests.Session()  # Reuse connections
        self.lock = threading.Lock()
    
    def download_image_from_url(self, image_url: str, max_retries=3, timeout=30) -> str:
        """
        Tải ảnh từ URL (Cloudinary) và lưu tạm thời
        Returns: đường dẫn file local
        """
        for attempt in range(max_retries):
            try:
                print(f"  Downloading {image_url} (attempt {attempt + 1}/{max_retries})")
                
                # Tạo tên file unique
                file_extension = self._get_file_extension(image_url)
                filename = f"{uuid.uuid4()}{file_extension}"
                local_path = os.path.join(self.temp_dir, filename)
                
                # Tải ảnh từ URL với timeout
                response = requests.get(image_url, stream=True, timeout=timeout)
                response.raise_for_status()
                
                # Lưu file
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                print(f"  ✓ Downloaded to {local_path}")
                return local_path
                
            except Exception as e:
                print(f"  ✗ Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)  # Wait before retry
                else:
                    print(f"Lỗi khi tải ảnh từ {image_url} sau {max_retries} lần thử: {e}")
                    raise e
    
    def download_multiple_images(self, image_urls: List[str]) -> List[str]:
        """
        Tải nhiều ảnh từ URLs
        Returns: danh sách đường dẫn local
        """
        local_paths = []
        for i, url in enumerate(image_urls):
            print(f"Downloading image {i+1}/{len(image_urls)}")
            local_path = self.download_image_from_url(url)
            local_paths.append(local_path)
            
            # Log progress every 20 images
            if (i + 1) % 20 == 0:
                print(f"Progress: {i+1}/{len(image_urls)} images downloaded")
                
        return local_paths
    
    def download_single_image(self, url_label_tuple, timeout=10, max_retries=2):
        """Download single image with URL and label"""
        url, label = url_label_tuple
        
        # Create label directory
        label_dir = os.path.join(self.temp_dir, str(label))
        with self.lock:
            os.makedirs(label_dir, exist_ok=True)
        
        for attempt in range(max_retries):
            try:
                # Generate filename
                file_extension = self._get_file_extension(url)
                filename = f"{uuid.uuid4()}{file_extension}"
                local_path = os.path.join(label_dir, filename)
                
                # Download with shorter timeout
                response = self.session.get(url, stream=True, timeout=timeout)
                response.raise_for_status()
                
                # Save file
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                return (label, local_path, True, f"✓ Downloaded {url}")
                
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(1)  # Short wait
                else:
                    return (label, None, False, f"✗ Failed {url}: {str(e)[:100]}")
    
    def download_and_organize_by_labels_fast(self, image_urls: List[str], labels: List[str], max_workers=8) -> Dict[str, List[str]]:
        """
        Tải ảnh parallel và organize theo labels
        Skip failed downloads and continue with successful ones
        """
        if len(image_urls) != len(labels):
            raise ValueError("Number of URLs must match number of labels")
            
        print(f"Starting parallel download with {max_workers} workers...")
        organized_paths = {}
        successful_downloads = 0
        failed_downloads = 0
        
        # Prepare URL-label pairs
        url_label_pairs = list(zip(image_urls, labels))
        
        # Download in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.download_single_image, pair) for pair in url_label_pairs]
            
            for i, future in enumerate(futures):
                result = future.result()
                label, local_path, success, message = result
                
                if success and local_path:
                    # Add to organized dict
                    if label not in organized_paths:
                        organized_paths[label] = []
                    organized_paths[label].append(local_path)
                    successful_downloads += 1
                else:
                    failed_downloads += 1
                
                # Progress logging
                if (i + 1) % 20 == 0:
                    print(f"Progress: {i+1}/{len(url_label_pairs)} processed, ✓{successful_downloads} ✗{failed_downloads}")
        
        print(f"Download completed: ✓{successful_downloads} successful, ✗{failed_downloads} failed")
        print(f"Labels with images: {[(label, len(paths)) for label, paths in organized_paths.items()]}")
        
        # Check if we have enough images per label
        min_images_per_label = 3  # Minimum for training
        valid_labels = {label: paths for label, paths in organized_paths.items() if len(paths) >= min_images_per_label}
        
        if len(valid_labels) < 2:
            raise ValueError(f"Need at least 2 labels with {min_images_per_label}+ images each. Got: {len(valid_labels)}")
            
        print(f"Valid labels for training: {len(valid_labels)}")
        return valid_labels

    def download_and_organize_by_labels(self, image_urls: List[str], labels: List[str]) -> Dict[str, List[str]]:
        """
        Fallback method - use fast parallel download
        """
        return self.download_and_organize_by_labels_fast(image_urls, labels)
    
    def _get_file_extension(self, url: str) -> str:
        """Lấy phần mở rộng file từ URL"""
        parsed_url = urlparse(url)
        path = parsed_url.path
        
        # Lấy extension từ URL hoặc default .jpg
        if '.' in path:
            return path[path.rfind('.'):]
        else:
            return '.jpg'
    
    def cleanup_temp_files(self, file_paths: List[str] = None):
        """Xóa các file tạm sau khi train xong"""
        if file_paths:
            # Xóa specific files
            for file_path in file_paths:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f"Không thể xóa file {file_path}: {e}")
        else:
            # Xóa toàn bộ temp directory
            import shutil
            try:
                if os.path.exists(self.temp_dir):
                    shutil.rmtree(self.temp_dir)
                    print(f"Đã xóa thư mục tạm: {self.temp_dir}")
            except Exception as e:
                print(f"Không thể xóa thư mục {self.temp_dir}: {e}")
    
    def load_image_as_array(self, image_path: str) -> np.ndarray:
        """Load ảnh thành numpy array để train"""
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Không thể đọc ảnh từ {image_path}")
        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img 
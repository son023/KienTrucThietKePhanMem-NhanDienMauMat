import os
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import uuid
import json
from pathlib import Path

# Configure Cloudinary (thay thông tin của bạn)
cloudinary.config(
    cloud_name="drgxm636o",  # Thay bằng cloud_name của bạn
    api_key="481389927974111",  # Thay bằng api_key của bạn
    api_secret="mWzxNSNVs7eFmbcGgpRNhosMZNQ"  # Thay bằng api_secret của bạn
)

def upload_all_samples():
    """
    Upload tất cả ảnh mắt từ thư mục samples lên Cloudinary
    """
    samples_dir = Path("statics/samples")
    upload_results = {}
    sql_inserts = []
    
    # Duyệt qua từng thư mục nhân viên (1-40)
    for member_folder in range(1, 41):
        member_path = samples_dir / str(member_folder)
        
        if not member_path.exists():
            print(f"Thư mục {member_folder} không tồn tại")
            continue
            
        print(f"Đang upload ảnh cho nhân viên {member_folder}...")
        
        member_results = []
        
        # Duyệt qua tất cả ảnh trong thư mục
        for image_file in member_path.glob("*.jpg"):
            try:
                # Tạo public_id duy nhất
                public_id = f"eye_samples/{member_folder}/{image_file.stem}_{uuid.uuid4().hex[:8]}"
                
                # Upload lên Cloudinary
                result = cloudinary.uploader.upload(
                    str(image_file),
                    public_id=public_id,
                    folder="eye_recognition_samples",
                    resource_type="image",
                    quality="auto",
                    width=224,
                    height=224,
                    crop="fill"
                )
                
                member_results.append({
                    "original_filename": image_file.name,
                    "cloudinary_url": result["secure_url"],
                    "public_id": result["public_id"]
                })
                
                print(f"  ✓ {image_file.name} -> {result['secure_url']}")
                
            except Exception as e:
                print(f"  ✗ Lỗi upload {image_file.name}: {e}")
        
        upload_results[member_folder] = member_results
    
    # Lưu kết quả vào file JSON
    with open("upload_results.json", "w", encoding="utf-8") as f:
        json.dump(upload_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Hoàn thành upload! Kết quả lưu trong upload_results.json")
    return upload_results

def generate_sql_from_upload_results(upload_results_file="upload_results.json"):
    """
    Tạo SQL INSERT statements từ kết quả upload
    """
    try:
        with open(upload_results_file, "r", encoding="utf-8") as f:
            upload_results = json.load(f)
    except FileNotFoundError:
        print("Không tìm thấy file upload_results.json. Hãy chạy upload trước!")
        return
    
    # Base UUIDs cho members (cần khớp với script database)
    base_member_uuids = [
        f"550e8400-e29b-41d4-a716-4466554400{i:02d}" for i in range(1, 41)
    ]
    
    sql_statements = []
    sql_statements.append("-- Thêm dữ liệu EyeRecognitionSample với Cloudinary URLs")
    sql_statements.append("INSERT INTO tblEyeRecognitionSample (id, memberId, eyeImageLink, label, isActive, captureDate) VALUES")
    
    insert_values = []
    
    for member_num, images in upload_results.items():
        member_idx = int(member_num) - 1
        member_uuid = base_member_uuids[member_idx]
        
        for image_info in images:
            sample_uuid = str(uuid.uuid4())
            cloudinary_url = image_info["cloudinary_url"]
            
            insert_values.append(
                f"('{sample_uuid}', '{member_uuid}', '{cloudinary_url}', '{member_uuid}', true, CURRENT_TIMESTAMP)"
            )
    
    # Join tất cả values
    sql_statements.append(",\n".join(insert_values) + ";")
    
    # Lưu vào file SQL
    sql_content = "\n".join(sql_statements)
    with open("eye_samples_insert.sql", "w", encoding="utf-8") as f:
        f.write(sql_content)
    
    print("✓ SQL statements đã được tạo trong eye_samples_insert.sql")
    return sql_content

if __name__ == "__main__":
    print("=== CLOUDINARY UPLOADER ===")
    print("1. Upload all samples")
    print("2. Generate SQL from upload results")
    print("3. Upload and generate SQL")
    
    choice = input("Chọn (1/2/3): ").strip()
    
    if choice == "1":
        upload_all_samples()
    elif choice == "2":
        generate_sql_from_upload_results()
    elif choice == "3":
        results = upload_all_samples()
        generate_sql_from_upload_results()
    else:
        print("Lựa chọn không hợp lệ!") 
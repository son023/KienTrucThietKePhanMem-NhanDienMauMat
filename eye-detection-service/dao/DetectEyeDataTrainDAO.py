# dao/DetectEyeDataTrainDAO.py
from typing import List, Optional
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from entity.DetectEyeDataTrain import DetectEyeDataTrain
from entity.DetectEyeData import DetectEyeData
from dao.DetectEyeDataDAO import DetectEyeDataDAO
from db_connection import get_connection

class DetectEyeDataTrainDAO:
    def __init__(self):
        self.conn = None
        self.detect_eye_data_dao = DetectEyeDataDAO()
    
    def get_all(self) -> List[DetectEyeDataTrain]:
        self.conn = get_connection()
        
        items = []
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM tblDetectEyeDataTrain"
                cursor.execute(query)
                rows = cursor.fetchall()
                
                for row in rows:
                    eye_datas = self.detect_eye_data_dao.get_by_train_id(row["id"])
                    item = DetectEyeDataTrain.from_db_row(row, eye_datas)
                    items.append(item)
                
        except Error as e:
            print(f"Lỗi khi lấy danh sách dữ liệu huấn luyện: {e}")
            raise e
        finally:
            if self.conn:
                self.conn.close()
        
        return items
    
    def get_by_id(self, item_id: int) -> Optional[DetectEyeDataTrain]:
        self.conn = get_connection()
        
        item = None
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM tblDetectEyeDataTrain WHERE id = %s"
                cursor.execute(query, (item_id,))
                row = cursor.fetchone()
                
                if row:
                    eye_datas = self.detect_eye_data_dao.get_by_train_id(row["id"])
                    item = DetectEyeDataTrain.from_db_row(row, eye_datas)
                
        except Error as e:
            print(f"Lỗi khi lấy dữ liệu huấn luyện theo ID: {e}")
            raise e
        finally:
            if self.conn:
                self.conn.close()
        
        return item
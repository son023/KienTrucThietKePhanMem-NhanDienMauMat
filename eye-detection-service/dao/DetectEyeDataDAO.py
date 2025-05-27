# dao/DetectEyeDataDAO.py
from typing import List, Optional
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from entity.DetectEyeData import DetectEyeData
from db_connection import get_connection

class DetectEyeDataDAO:
    def __init__(self):
        self.conn = None
    
    def get_by_train_id(self, train_id: int) -> List[DetectEyeData]:
        self.conn = get_connection()
        
        items = []
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM tblDetectEyeData WHERE tblDetectEyeDataTrainId = %s"
                cursor.execute(query, (train_id,))
                rows = cursor.fetchall()
                
                items = [DetectEyeData.from_db_row(row) for row in rows]
                
        except Error as e:
            print(f"Lỗi khi lấy dữ liệu mắt theo ID huấn luyện: {e}")
            raise e
        finally:
            if self.conn:
                self.conn.close()
        
        return items

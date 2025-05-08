# dao/DetectEyeDataDAO.py
from typing import List, Optional
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from entity.DetectEyeData import DetectEyeData
from db_connection import get_connection

class DetectEyeDataDAO:
    def __init__(self):
        self.conn = None
    
    def get_all(self) -> List[DetectEyeData]:
        self.conn = get_connection()
        
        items = []
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM tblDetectEyeData"
                cursor.execute(query)
                rows = cursor.fetchall()
                
                items = [DetectEyeData.from_db_row(row) for row in rows]
                
        except Error as e:
            print(f"Lỗi khi lấy danh sách dữ liệu mắt: {e}")
            raise e
        finally:
            if self.conn:
                self.conn.close()
        
        return items
    
    def get_by_id(self, item_id: int) -> Optional[DetectEyeData]:
        self.conn = get_connection()
        
        item = None
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM tblDetectEyeData WHERE id = %s"
                cursor.execute(query, (item_id,))
                row = cursor.fetchone()
                
                if row:
                    item = DetectEyeData.from_db_row(row)
                
        except Error as e:
            print(f"Lỗi khi lấy dữ liệu mắt theo ID: {e}")
            raise e
        finally:
            if self.conn:
                self.conn.close()
        
        return item
    
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

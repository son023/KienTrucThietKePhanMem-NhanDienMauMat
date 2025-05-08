# dao/EyeDetectionModelDAO.py
from typing import List, Optional
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from entity.EyeDetectionModel import EyeDetectionModel
from dao.TrainDetectionHistoryDAO import TrainDetectionHistoryDAO
from db_connection import get_connection

class EyeDetectionModelDAO:
    def __init__(self):
        self.conn = None
        self.train_history_dao = TrainDetectionHistoryDAO()
    
    def get_all(self, active_only: bool = True) -> List[EyeDetectionModel]:
        self.conn = get_connection()
        
        items = []
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM tblEyeDetectionModel"
                if active_only:
                    query += " WHERE isactive = true"
                cursor.execute(query)
                rows = cursor.fetchall()
                
                for row in rows:
                    history = self.train_history_dao.get_by_model_id(row["id"])
                    item = EyeDetectionModel.from_db_row(row, history)
                    items.append(item)
                
        except Error as e:
            print(f"Lỗi khi lấy danh sách mô hình phát hiện mắt: {e}")
            raise e
        finally:
            if self.conn:
                self.conn.close()
        
        return items
    
    def get_by_id(self, model_id: int) -> Optional[EyeDetectionModel]:
        self.conn = get_connection()
        
        item = None
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM tblEyeDetectionModel WHERE id = %s"
                cursor.execute(query, (model_id,))
                row = cursor.fetchone()
                
                if row:
                    history = self.train_history_dao.get_by_model_id(row["id"])
                    item = EyeDetectionModel.from_db_row(row, history)
                
        except Error as e:
            print(f"Lỗi khi lấy mô hình phát hiện mắt theo ID: {e}")
            raise e
        finally:
            if self.conn:
                self.conn.close()
        
        return item
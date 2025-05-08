# dao/TrainDetectionHistoryDAO.py
from typing import List, Optional
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
from entity.TrainDetectionHistory import TrainDetectionHistory
from dao.DetectEyeDataTrainDAO import DetectEyeDataTrainDAO
from db_connection import get_connection

class TrainDetectionHistoryDAO:
    def __init__(self):
        self.conn = None
        self.data_train_dao = DetectEyeDataTrainDAO()
    
    def get_all(self) -> List[TrainDetectionHistory]:
        self.conn = get_connection()
        
        items = []
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM TrainDetectionHistory"
                cursor.execute(query)
                rows = cursor.fetchall()
                
                for row in rows:
                    data_train = self.data_train_dao.get_by_id(row["tbldetecteyedatatrainid"])
                    item = TrainDetectionHistory.from_db_row(row, data_train)
                    items.append(item)
                
        except Error as e:
            print(f"Lỗi khi lấy danh sách lịch sử huấn luyện: {e}")
            raise e
        finally:
            if self.conn:
                self.conn.close()
        
        return items
    
    def get_by_id(self, item_id: int) -> Optional[TrainDetectionHistory]:
        self.conn = get_connection()
        
        item = None
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM TrainDetectionHistory WHERE id = %s"
                cursor.execute(query, (item_id,))
                row = cursor.fetchone()
                
                if row:
                    data_train = self.data_train_dao.get_by_id(row["tbldetecteyedatatrainid"])
                    item = TrainDetectionHistory.from_db_row(row, data_train)
                
        except Error as e:
            print(f"Lỗi khi lấy lịch sử huấn luyện theo ID: {e}")
            raise e
        finally:
            if self.conn:
                self.conn.close()
        
        return item
    
    def get_by_model_id(self, model_id: int) -> List[TrainDetectionHistory]:
        self.conn = get_connection()
        
        items = []
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM TrainDetectionHistory WHERE tblEyeDetectionModelId = %s"
                cursor.execute(query, (model_id,))
                rows = cursor.fetchall()
                
                for row in rows:
                    data_train = self.data_train_dao.get_by_id(row["tbldetecteyedatatrainid"])
                    item = TrainDetectionHistory.from_db_row(row, data_train)
                    items.append(item)
                
        except Error as e:
            print(f"Lỗi khi lấy lịch sử huấn luyện theo ID mô hình: {e}")
            raise e
        finally:
            if self.conn:
                self.conn.close()
        
        return items


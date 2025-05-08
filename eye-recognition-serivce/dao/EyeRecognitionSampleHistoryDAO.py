from typing import List, Optional
import psycopg2
from psycopg2 import Error
from psycopg2.extras import DictCursor, RealDictCursor
from entity.EyeRecognitionSampleHistory import EyeRecognitionSampleHistory
from entity.EyeRecognitionSample import EyeRecognitionSample
from dao.EyeRecognitionSampleDAO import EyeRecognitionSampleDAO
from db_connection import get_connection

class EyeRecognitionSampleHistoryDAO:

    @staticmethod
    async def get_all_by_model_id(model_id: int) -> List[EyeRecognitionSampleHistory]:
        conn = get_connection()
        
        histories = []
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM tblEyeRecognitionSampleHistory where tblrecognitionmodelid = %s"
                
                cursor.execute(query,(model_id,))
                rows = cursor.fetchall()
                
                for row in rows:
                    sample_query = """
                        SELECT s.* 
                        FROM tblEyeRecognitionSample s
                        JOIN tblEyeRecognitionSampleHistory h ON s.id = h.tblEyeRecognitionSampleid
                        WHERE h.id = %s
                    """
                    cursor.execute(sample_query, (row["id"],))
                    sample_row = cursor.fetchone()
                    sample = None
                    
                    if sample_row:
                        sample = EyeRecognitionSample.from_db_row(sample_row)
                    
                    history = EyeRecognitionSampleHistory.from_db_row(row, sample)
                    histories.append(history)
                
        except Error as e:
            print(f"Lỗi khi lấy danh sách lịch sử mẫu: {e}")
            raise e
        finally:
            if conn:
                conn.close()
        
        return histories
    
    @staticmethod
    async def get_by_id(history_id: int) -> Optional[EyeRecognitionSampleHistory]:
        conn = get_connection()
        
        history = None
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM tblEyeRecognitionSampleHistory WHERE id = %s"
                cursor.execute(query, (history_id,))
                row = cursor.fetchone()
                
                if row:
                    sample_query = """
                        SELECT s.* 
                        FROM tblEyeRecognitionSample s
                        JOIN tblEyeRecognitionSampleHistory h ON s.id = h.tblEyeRecognitionSampleid
                        WHERE h.id = %s
                    """
                    cursor.execute(sample_query, (history_id,))
                    sample_row = cursor.fetchone()
                    sample = None
                    
                    if sample_row:
                        sample = EyeRecognitionSample.from_db_row(sample_row)
                    
                    history = EyeRecognitionSampleHistory.from_db_row(row, sample)
            
        except Error as e:
            print(f"Lỗi khi lấy lịch sử mẫu theo ID: {e}")
            raise e
        finally:
            if conn:
                conn.close()
        
        return history
    
    @staticmethod
    async def create(history: EyeRecognitionSampleHistory, modelId:int):
        conn = get_connection()
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                insert_query = """
                    INSERT INTO tbleyerecognitionsamplehistory (notes, tbleyerecognitionsampleid, tblrecognitionmodelid) 
                    VALUES (%s, %s, %s) 
                    RETURNING id, notes
                """
                cursor.execute(insert_query, (history.notes, history.eyeRecognitionSample.id, modelId))
                conn.commit()
                
        except Error as e:
            conn.rollback()
            print(f"Lỗi khi tạo lịch sử mẫu: {e}")
            raise e
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    async def delete(history_id: int) -> bool:
        conn = get_connection()
        
        try:
            with conn.cursor() as cursor:
                delete_query = """
                    DELETE FROM tblEyeRecognitionSampleHistory
                    WHERE id = %s
                """
                cursor.execute(delete_query, (history_id,))
                
                conn.commit()
                return True
                
        except Error as e:
            conn.rollback()
            print(f"Lỗi khi xóa lịch sử mẫu: {e}")
            raise e
        finally:
            if conn:
                conn.close()
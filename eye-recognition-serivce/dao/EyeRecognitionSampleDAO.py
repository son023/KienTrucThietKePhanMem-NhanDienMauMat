from typing import List, Optional
from psycopg2 import Error
from psycopg2.extras import RealDictCursor  
from datetime import datetime
from entity.EyeRecognitionSample import EyeRecognitionSample
from db_connection import get_connection

class EyeRecognitionSampleDAO:
    
    @staticmethod
    def get_by_id(sample_id: int) -> Optional[EyeRecognitionSample]:
        conn = get_connection()
        
        sample = None
        try:
            with conn.cursor(cursor_factory=RealDictCursor  ) as cursor:
                query = "SELECT * FROM tblEyeRecognitionSample WHERE id = %s"
                cursor.execute(query, (sample_id,))
                row = cursor.fetchone()
                
                if row:
                    sample = EyeRecognitionSample.from_db_row(row)
                
        except Error as e:
            print(f"Lỗi khi lấy mẫu theo ID: {e}")
            raise e
        finally:
            if conn:
                conn.close()
        
        return sample
    
    @staticmethod
    def get_by_member_id(member_id: int) -> List[EyeRecognitionSample]:
        conn = get_connection()
        
        samples = []
        try:
            with conn.cursor(cursor_factory=RealDictCursor  ) as cursor:
                query = "SELECT * FROM tblEyeRecognitionSample WHERE memberid = %s"
                cursor.execute(query, (member_id,))
                rows = cursor.fetchall()
                
                samples = [EyeRecognitionSample.from_db_row(row) for row in rows]
        except Error as e:
            print(f"Lỗi khi lấy mẫu theo ID thành viên: {e}")
            raise e
        finally:
            if conn:
                conn.close()
        
        return samples
    
    @staticmethod
    async def is_member_has_enough_samples(memberId:int) -> bool:
        conn = get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT COUNT(*) FROM tblEyeRecognitionSample WHERE memberid = %s"
                
                cursor.execute(query,(memberId,))
                row = cursor.fetchone()
                sample_count  = row['count']
                return  sample_count > 1
        except Error as e:
            print(f"Lỗi khi đếm số mẫu của thành viên theo ID thành viên: {e}")
            raise e
        finally:
            if conn:
                conn.close()
 
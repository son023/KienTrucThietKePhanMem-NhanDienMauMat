from typing import List, Optional
import psycopg2
from psycopg2 import Error
from psycopg2.extras import DictCursor, RealDictCursor
from entity.EyeRecognitionModel import EyeRecognitionModel
from entity.EyeRecognitionSampleHistory import EyeRecognitionSampleHistory
from dao.EyeRecognitionSampleHistoryDAO import EyeRecognitionSampleHistoryDAO
from db_connection import get_connection
import json
from datetime import datetime

class EyeRecognitionModelDAO:

    
    @staticmethod
    async def get_all(active_only: bool = True) -> List[EyeRecognitionModel]:
        conn = get_connection()
        
        models = []
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM tblEyeRecognitionModel"
                if active_only:
                    query += " WHERE isactive = true"
                cursor.execute(query)
                rows = cursor.fetchall()
                
                for row in rows:    
                    model = EyeRecognitionModel(
                        id=row["id"],
                        modelLink=row["modellink"],
                        eyeModelName=row["eyemodelname"],
                        eyeRecognitionSampleTrain=[],
                        accuracy=row["accuracy"],
                        isActive=row["isactive"],
                        epochs=row["epochs"],
                        learningRate=row["learningrate"],
                        imageSize=row["imagesize"],
                        batchSize=row["batchsize"],
                        mappingLabel=row["mappinglabel"],
                        createDate=row["createdate"]
                    )
                    models.append(model)
                
        except Error as e:
            print(f"Lỗi khi lấy danh sách mô hình: {e}")
            raise e
        finally:
            if conn:
                conn.close()
        
        return models
    
    @staticmethod
    async def get_by_id(model_id: int) -> Optional[EyeRecognitionModel]:
        conn = get_connection()
        
        model = None
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM tblEyeRecognitionModel WHERE id = %s"
                cursor.execute(query, (model_id,))
                row = cursor.fetchone()
                
                if row:
                    model = EyeRecognitionModel(
                        id=row["id"],
                        modelLink=row["modellink"],
                        eyeModelName=row["eyemodelname"],
                        eyeRecognitionSampleTrain=[],
                        accuracy=row["accuracy"],
                        isActive=row["isactive"],
                        epochs=row["epochs"],
                        learningRate=row["learningrate"],
                        imageSize=row["imagesize"],
                        batchSize=row["batchsize"],
                        mappingLabel=row["mappinglabel"],
                        createDate=row["createdate"]
                    )
            
        except Error as e:
            print(f"Lỗi khi lấy mô hình theo ID: {e}")
            raise e
        finally:
            if conn:
                conn.close()
        
        return model
    
    @staticmethod
    async def create(model: EyeRecognitionModel) -> EyeRecognitionModel:
        conn = get_connection()
        
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                # Tạo bản ghi mô hình mới
                insert_query = """
                    INSERT INTO tblEyeRecognitionModel (
                        modellink, eyemodelname, accuracy, isactive, 
                        epochs, learningrate, imagesize, batchsize, 
                        mappinglabel, createdate
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                    RETURNING id
                """
                cursor.execute(insert_query, (
                    model.modelLink, 
                    model.eyeModelName, 
                    model.accuracy, 
                    model.isActive, 
                    model.epochs, 
                    model.learningRate, 
                    model.imageSize, 
                    model.batchSize, 
                    model.mappingLabel, 
                    datetime.now() if not model.createDate else model.createDate
                ))
                new_model_row = cursor.fetchone()
                conn.commit()
                # Lấy ID mới được tạo
                new_model_id = new_model_row["id"]
                
                
                print(new_model_id)
                # Tạo các bản ghi liên kết với lịch sử mẫu
                for history in model.eyeRecognitionSampleTrain:
                    await EyeRecognitionSampleHistoryDAO.create(history,new_model_id)
                
                # Trả về đối tượng mô hình đã được tạo
                return await EyeRecognitionModelDAO.get_by_id(new_model_id)
                
        except Error as e:
            conn.rollback()
            print(f"Lỗi khi tạo mô hình: {e}")
            raise e
        finally:
            if conn:
                conn.close()
    

    @staticmethod
    async def delete(model_id: int) -> bool:
        conn = get_connection()
        
        try:
            with conn.cursor() as cursor:
                # Xóa tất cả các liên kết mô hình-lịch sử
                delete_links_query = """
                    DELETE FROM tblEyeRecognitionModelHistory
                    WHERE modelid = %s
                """
                cursor.execute(delete_links_query, (model_id,))
                
                # Xóa bản ghi mô hình
                delete_query = """
                    DELETE FROM tblEyeRecognitionModel
                    WHERE id = %s
                """
                cursor.execute(delete_query, (model_id,))
                
                conn.commit()
                return True
                
        except Error as e:
            conn.rollback()
            print(f"Lỗi khi xóa mô hình: {e}")
            raise e
        finally:
            if conn:
                conn.close()
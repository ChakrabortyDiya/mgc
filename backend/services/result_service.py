from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.models import ResultData


class ResultService:
    @staticmethod
    def get_results(db: Session):
        return db.query(ResultData).all()

    @staticmethod
    def create_result(db: Session, result_data):
        new_result = ResultData(name=result_data.name,
                                json_data=result_data.json_data)
        db.add(new_result)
        db.commit()
        db.refresh(new_result)
        return new_result

    @staticmethod
    def get_result_by_id(db: Session, result_id: int):
        result = db.query(ResultData).filter(
            ResultData.id == result_id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Result not found")
        return result

    @staticmethod
    def delete_result(db: Session, result_id: int):
        result = db.query(ResultData).filter(
            ResultData.id == result_id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Result not found")
        db.delete(result)
        db.commit()
        return {"message": "Result deleted successfully"}

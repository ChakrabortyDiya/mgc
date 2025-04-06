from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import ResultData
from services.result_service import ResultService
from pydantic import BaseModel

router = APIRouter()


class ResultCreate(BaseModel):
    name: str
    json_data: str


@router.get("/results", response_model=list[ResultCreate])
def get_all_results(db: Session = Depends(get_db)):
    return ResultService.get_results(db)


@router.post("/results", response_model=ResultCreate)
def create_result(result: ResultCreate, db: Session = Depends(get_db)):
    return ResultService.create_result(db, result)


@router.get("/results/{result_id}", response_model=ResultCreate)
def get_result(result_id: int, db: Session = Depends(get_db)):
    return ResultService.get_result_by_id(db, result_id)


@router.delete("/results/{result_id}")
def delete_result(result_id: int, db: Session = Depends(get_db)):
    return ResultService.delete_result(db, result_id)

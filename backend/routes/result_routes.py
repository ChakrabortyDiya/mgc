from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from utils import TableData
from services.result_service import DashboardService

router = APIRouter()

@router.post("/dashboard/data")
def get_dashboard_data(data: TableData, db: Session = Depends(get_db)):
    return DashboardService.fetch_grouped_results(db, data)

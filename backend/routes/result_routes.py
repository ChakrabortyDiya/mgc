from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
# updated import if renamed to `db.py` per earlier changes
from database.db import SessionLocal
from utils import TableData
from services.result_service import DashboardService

router = APIRouter()

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/dashboard/data")
def get_dashboard_data(data: TableData, db: Session = Depends(get_db)):
    return DashboardService.fetch_grouped_results(db, data)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import SessionLocal
from utils import TableData
from services.result_service import DashboardService
from plots.plot_to_json import PlotGenerator
from plots.scatter_to_json import ScatterPlotGenerator
from utils import MetricsPlotData
from fastapi import FastAPI, HTTPException
import json

router = APIRouter()

# Dependency
plot_generator = PlotGenerator()
scatterplot_generator = ScatterPlotGenerator()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard/test")
def test_api():
    """Endpoint to test API responsiveness."""
    try:
        return {"message": "API is working"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dashboard/data")
def get_dashboard_data(data: TableData, db: Session = Depends(get_db)):
    try:
        return DashboardService.fetch_grouped_results(db, data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dashboard/chart/barchart")
def get_plot(MetricsPlotData: MetricsPlotData):
    """Endpoint to generate a plot based on the provided data name."""
    try:
        data_name = MetricsPlotData.name
        json_data = plot_generator.generate_data_by_name(data_name)
        return json.loads(json_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/chart/scatterplot")
def get_scatter_plot():
    """Endpoint to generate a scatter plot based on the provided data."""
    try:
        return scatterplot_generator.generate_scatter_plot("data\\plot_metadata")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

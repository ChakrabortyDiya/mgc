import logging
from fastapi import APIRouter, Depends, HTTPException, FastAPI
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database.db import SessionLocal
from utils import TableData, MetricsPlotData
from services.result_service import DashboardService
from plots.plot_to_json import PlotGenerator
from plots.scatter_to_json import ScatterPlotGenerator
import plotly.graph_objects as go
import json

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

router = APIRouter()

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
        logger.error("Error in test_api", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dashboard/data")
def get_dashboard_data(data: TableData, db: Session = Depends(get_db)):
    logger.info("[INFO] Fetching dashboard data...")
    logger.info(f"[INFO] Data: {data}")
    try:
        return DashboardService.fetch_grouped_results(db, data)
    except Exception as e:
        logger.error("Error in get_dashboard_data", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dashboard/chart/barchart")
def get_plot(metrics_plot_data: MetricsPlotData):
    """Endpoint to generate a plot based on the provided data name."""
    try:
        data_name = metrics_plot_data.name
        json_data = plot_generator.generate_data_by_name(data_name)
        # Parse JSON string to dictionary and create figure
        fig_dict = json.loads(json_data)
        fig = go.Figure(fig_dict)
        html_plot = fig.to_html(full_html=False, include_plotlyjs="cdn")
        return HTMLResponse(content=html_plot)
    except Exception as e:
        logger.error("Error in get_plot (barchart)", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/dashboard/chart/scatterplot")
def get_scatter_plot():
    """Endpoint to generate a scatter plot based on the provided data."""
    try:
        scatter_data =  scatterplot_generator.generate_scatter_plot("data\\plot_metadata")
        fig_dict = json.loads(scatter_data)
        fig = go.Figure(fig_dict)
        html_plot = fig.to_html(full_html=False, include_plotlyjs="cdn")
        return HTMLResponse(content=html_plot)
    except Exception as e:
        logger.error("Error in get_scatter_plot", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

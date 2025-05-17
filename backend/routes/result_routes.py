import logging
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from database.db import db_dna, db_small_genomes # now using MongoDB databases from db.py
from utils import TableData, MetricsPlotData
from services.table_results import TabularData
from services.plot_to_json import PlotGenerator
from services.scatter_to_json import ScatterPlotGenerator
import plotly.graph_objects as go

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

router = APIRouter()

# Instantiate plot generators
plot_generator = PlotGenerator()
scatterplot_generator = ScatterPlotGenerator()

# Use the "results" collection from the DNA corpus database.
results_collection_dna = db_dna["results"]
results_collection_genome = db_small_genomes["results"]

@router.get("/dashboard/test")
def test_api():
    """Endpoint to test API responsiveness."""
    try:
        return {"message": "API is working"}
    except Exception as e:
        logger.error("Error in test_api", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dashboard/data")
def get_dashboard_data(data: TableData)->list:
    logger.info("[INFO] Fetching dashboard data...")
    logger.info(f"[INFO] Data: {data}")
    try:
        result_dna = TabularData.fetch_grouped_results(results_collection_dna, data)
        result_genome = TabularData.fetch_grouped_results(results_collection_genome, data)
        combined = result_dna + result_genome

        # Create a dict with a composite key
        # result_dict = {
        #     f"{item['Dataset ID']}_{item['Compressor']}_{item['Compressor Type']}": item
        #     for item in combined
        # }
        return combined
    except Exception as e:
        logger.error("Error in get_dashboard_data", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dashboard/chart/barchart")
def get_plot(metrics_plot_data: MetricsPlotData):
    """Endpoint to generate a plot (barchart) based on the provided data name."""
    try:
        logger.info("[INFO] Generating plot...")
        logger.info(f"[INFO] Metrics plot data: {metrics_plot_data}")
        benchmark_type = metrics_plot_data.genomeType
        data_name = metrics_plot_data.name
        # Normalize CPU names.
        if data_name == "compression_cpu":
            data_name = "compression_cpu_usage"
        elif data_name == "decompression_cpu":
            data_name = "decompression_cpu_usage"
        
        logger.info(f"[INFO] Generating plot for benchmark type: {benchmark_type}, data name: {data_name}")
        
        json_data = plot_generator.generate_data_by_name(benchmark_type, data_name)
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
        scatter_data = scatterplot_generator.generate_scatter_plot("data\\plot_metadata")
        fig_dict = json.loads(scatter_data)
        fig = go.Figure(fig_dict)
        html_plot = fig.to_html(full_html=False, include_plotlyjs="cdn")
        return HTMLResponse(content=html_plot)
    except Exception as e:
        logger.error("Error in get_scatter_plot", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

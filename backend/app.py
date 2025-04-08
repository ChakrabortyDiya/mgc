from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import subprocess
import json
import os
from dotenv import load_dotenv
from utils import ScatterPlotData, MetricsPlotData
from plots.plot_to_json import PlotGenerator
from routes import result_routes

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

plot_generator = PlotGenerator()


@app.get("/dashboard/test")
def test_api():
    """Endpoint to test API responsiveness."""
    return {"message": "API is working"}


@app.post("/dashboard/chart/barchart")
def get_plot(MetricsPlotData: MetricsPlotData):
    """Endpoint to generate a plot based on the provided data name."""
    try:
        data_name = MetricsPlotData.name
        json_data = plot_generator.generate_data_by_name(data_name)
        return json.loads(json_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(result_routes.router)
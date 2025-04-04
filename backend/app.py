from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import subprocess, json
from utils import ScatterPlotData, MetricsPlotData
from plots.plot_to_json import PlotGenerator

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

plot_generator = PlotGenerator()

@app.get("/dashboard/test")
def test_api():
    """
    Endpoint to test API responsiveness.
    """
    return {"message": "API is working"}

@app.post("/dashboard/chart/barchart")
def get_plot(MetricsPlotData: MetricsPlotData):
    """
    Endpoint to generate a plot based on the provided data name.    
    """
    try:
        data_name = MetricsPlotData.name
        json_data = plot_generator.generate_data_by_name(data_name)
        return json.loads(json_data)  # Return the JSON data as a response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

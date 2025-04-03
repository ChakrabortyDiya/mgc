from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import subprocess, json
from backend.utils import ScatterPlotData, MetricsPlotData
from backend.plots.plot_to_json import PlotGenerator

app = FastAPI()
plot_generator = PlotGenerator()

@app.post("/dashboard/plot")
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

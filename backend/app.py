from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import subprocess, json
from utils import ScatterPlotData, MetricsPlotData

app = FastAPI()

@app.get("dashboard/plot")
def get_plot(name: str):
    try:
        result = subprocess.run(["python", "plots/plot_to_csv.py", name],
                                capture_output=True, text=True)
        if result.returncode != 0:
            raise HTTPException(status_code=400, detail=result.stderr)
        json_output = json.loads(result.stdout)
        if isinstance(json_output, dict) and json_output.get("error"):
            raise HTTPException(status_code=400, detail=json_output["error"])
        return json_output
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Invalid JSON format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

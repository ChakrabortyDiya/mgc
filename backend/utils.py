from pydantic import BaseModel

class ScatterPlotData(BaseModel):
    name: str

class MetricsPlotData(BaseModel):
    name: str
from pydantic import BaseModel
from typing import List, Dict, Any

class ScatterPlotData(BaseModel):
    name: str

class MetricsPlotData(BaseModel):
    name: str
    
class TableData(BaseModel):
    id: List[str]
    comp_type: List[int]      #[0-s 1-p]
    comp_name: List[str]      #[s-zpaq,null/P]
    metric: List[str]          #col-names     
    
    
    
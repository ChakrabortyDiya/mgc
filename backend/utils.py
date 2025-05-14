from pydantic import BaseModel
from typing import List, Dict, Any

class ScatterPlotData(BaseModel):
    name: str

class MetricsPlotData(BaseModel):
    genomeType: str
    name: str
    
class TableData(BaseModel):
    id: List[str]
    comp_type: List[int]      #[0-s 1-p]
    # comp_name: Dict[str, str]      #[s-zpaq,null/P]
    standard_comp_name: List[str]      # standard compressor names
    proposed_comp_name: List[str]      # proposed compressor names
    metric: List[str]          # col-names
        
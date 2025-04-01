from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any

BaseClass = BaseModel
class DataModel(BaseClass):
    id: int
    name: str
    standard_compressor_settings: str
    proposed_compressor_settings: str
    table_contents: List[str]


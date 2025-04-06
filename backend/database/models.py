from sqlalchemy import Column, Integer, String
from .db import Base


class ResultData(Base):
    __tablename__ = "result_data"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    json_data = Column(String)  # Store JSON output

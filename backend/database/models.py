from sqlalchemy import Column, String, Float
from database.db import Base

class ResultComparison(Base):
    __tablename__ = "result_comparison"

    dataset_id = Column(String, primary_key=True)
    compressor = Column(String, primary_key=True)
    compressor_type = Column(String, primary_key=True)
    dataset_type = Column(String, default="dna")

    compression_ratio = Column(Float, default=0)
    compression_memory = Column(Float, default=0)
    compression_time = Column(Float, default=0)
    compression_cpu_usage = Column(Float, default=0)

    decompression_memory = Column(Float, default=0)
    decompression_time = Column(Float, default=0)
    decompression_cpu_usage = Column(Float, default=0)

from sqlalchemy import Table, MetaData
from sqlalchemy.orm import declarative_base
from database.db import engine

Base = declarative_base()
metadata = MetaData()

# Reflect the existing users table


class ResultComparison(Base):
    __table__ = Table("result_comparison", metadata, autoload_with=engine)

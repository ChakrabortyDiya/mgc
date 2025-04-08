# showdbs.py

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

# Use your actual PostgreSQL DATABASE_URL
DATABASE_URL = "postgresql://mgc_data_user:r5Y50xL907REXIaum4wZzVKYmLmOhdDv@dpg-cvnvej95pdvs73di55t0-a.oregon-postgres.render.com/mgc_data"

# Create engine and session
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def show_tables_and_columns():
    db = SessionLocal()
    try:
        inspector = inspect(db.bind)
        tables = inspector.get_table_names()

        if not tables:
            print("No tables found in the database.")
            return

        print("📋 Tables and columns in the PostgreSQL database:")
        for table_name in tables:
            print(f"\n🔹 Table: {table_name}")
            columns = inspector.get_columns(table_name)
            for column in columns:
                print(
                    f"   ├─ Column: {column['name']:<20} Type: {column['type']} | Nullable: {column['nullable']}")
    finally:
        db.close()


if __name__ == "__main__":
    show_tables_and_columns()

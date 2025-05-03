# # showdbs.py

# from sqlalchemy import create_engine, inspect
# from sqlalchemy.orm import sessionmaker

# # Use your actual PostgreSQL DATABASE_URL
# DATABASE_URL = "postgresql://mgc_data_user:r5Y50xL907REXIaum4wZzVKYmLmOhdDv@dpg-cvnvej95pdvs73di55t0-a.oregon-postgres.render.com/mgc_data"

# # Create engine and session
# engine = create_engine(DATABASE_URL, echo=False)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def show_tables_and_columns():
#     db = SessionLocal()
#     try:
#         inspector = inspect(db.bind)
#         tables = inspector.get_table_names()

#         if not tables:
#             print("No tables found in the database.")
#             return

#         print("📋 Tables and columns in the PostgreSQL database:")
#         for table_name in tables:
#             print(f"\n🔹 Table: {table_name}")
#             columns = inspector.get_columns(table_name)
#             for column in columns:
#                 print(
#                     f"   ├─ Column: {column['name']:<20} Type: {column['type']} | Nullable: {column['nullable']}")
#     finally:
#         db.close()


# if __name__ == "__main__":
#     show_tables_and_columns()


import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

def show_databases_and_collections():
    try:
        client = MongoClient(MONGODB_URI)
        # List all database names.
        db_names = client.list_database_names()
        if not db_names:
            print("No databases found.")
            return
        print("📋 Databases and collections in MongoDB:")
        for db_name in db_names:
            print(f"\n🔹 Database: {db_name}")
            db = client[db_name]
            collections = db.list_collection_names()
            if not collections:
                print("   No collections found.")
                continue
            for coll in collections:
                print(f"   ├─ Collection: {coll}")
                # Display sample document keys, if any.
                sample_doc = db[coll].find_one()
                if sample_doc:
                    print(f"       └─ Sample document keys: {list(sample_doc.keys())}")
                else:
                    print("       └─ Collection is empty!")
    except Exception as e:
        print(f"Error showing databases: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    show_databases_and_collections()
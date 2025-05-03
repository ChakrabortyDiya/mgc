# import os
# import psycopg2
# from dotenv import load_dotenv

# load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL")


# def reset_database():
#     try:
#         conn = psycopg2.connect(DATABASE_URL)
#         cur = conn.cursor()

#         print(" Dropping old tables if they exist...")
#         cur.execute("DROP TABLE IF EXISTS result_comparison CASCADE;")
#         cur.execute("DROP TABLE IF EXISTS dashboard_data CASCADE;")

#         print(" Creating new tables...")

#         cur.execute("""
#             CREATE TABLE result_comparison (
#                 dataset_id TEXT NOT NULL,
#                 compressor TEXT NOT NULL,
#                 compressor_type TEXT NOT NULL,
#                 dataset_type TEXT DEFAULT 'dna',

#                 compression_ratio DOUBLE PRECISION DEFAULT 0,
#                 compression_memory DOUBLE PRECISION DEFAULT 0,
#                 compression_time DOUBLE PRECISION DEFAULT 0,
#                 compression_cpu_usage DOUBLE PRECISION DEFAULT 0,

#                 decompression_memory DOUBLE PRECISION DEFAULT 0,
#                 decompression_time DOUBLE PRECISION DEFAULT 0,
#                 decompression_cpu_usage DOUBLE PRECISION DEFAULT 0,

#                 original_size DOUBLE PRECISION DEFAULT 0,
#                 compressed_size DOUBLE PRECISION DEFAULT 0,

#                 PRIMARY KEY (dataset_id, compressor, compressor_type)
#             );
#         """)

#         cur.execute("""
#             CREATE TABLE dashboard_data (
#             dataset_id TEXT PRIMARY KEY,
#             dataset_type TEXT DEFAULT 'dna'
#             );
#         """)

#         conn.commit()
#         print("Tables recreated successfully!")

#         # Show tables and columns
#         print("\nTables and columns in the current database:")
#         cur.execute("""
#             SELECT table_name
#             FROM information_schema.tables
#             WHERE table_schema = 'public'
#             ORDER BY table_name;
#         """)
#         tables = cur.fetchall()
#         for (table_name,) in tables:
#             print(f"\nTable: {table_name}")
#             cur.execute(f"""
#                 SELECT column_name, data_type
#                 FROM information_schema.columns
#                 WHERE table_name = %s
#                 ORDER BY ordinal_position;
#             """, (table_name,))
#             columns = cur.fetchall()
#             for col_name, data_type in columns:
#                 print(f"  - {col_name} ({data_type})")

#     except Exception as e:
#         print(f"Error setting up database: {e}")
#     finally:
#         cur.close()
#         conn.close()


# if __name__ == "__main__":
#     reset_database()


import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

# Define the two database names.
DATABASE_NAMES = [
    "result_less_repetitive_dna_corpus_raw",
    "result_less_repetitive_small_genomes_raw"
]

# Define the collection name that will be used in both databases.
COLLECTION_NAME = "results"

def reset_databases():
    try:
        client = MongoClient(MONGODB_URI)

        for db_name in DATABASE_NAMES:
            db = client[db_name]
            print(f"Processing database: {db_name}")
            
            # Drop the 'results' collection if it exists.
            if COLLECTION_NAME in db.list_collection_names():
                db.drop_collection(COLLECTION_NAME)
                print(f"  Dropped collection '{COLLECTION_NAME}' from database '{db_name}'")
            
            # Create the 'results' collection.
            db.create_collection(COLLECTION_NAME)
            print(f"  Created collection '{COLLECTION_NAME}' in database '{db_name}'")
            
            # Display collections in the current database.
            print(f"  Collections in '{db_name}':")
            for coll in db.list_collection_names():
                print("   -", coll)
                sample_doc = db[coll].find_one()
                if sample_doc:
                    print("      Sample document keys:", list(sample_doc.keys()))
                else:
                    print("      Collection is empty!")
                    
    except Exception as e:
        print(f"Error setting up databases: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    reset_databases()
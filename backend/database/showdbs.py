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
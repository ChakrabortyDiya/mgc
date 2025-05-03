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
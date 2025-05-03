# from sqlalchemy import Table, MetaData
# from sqlalchemy.orm import declarative_base
# from database.db import engine

# Base = declarative_base()
# metadata = MetaData()

# # Reflect the existing users table


# class ResultComparison(Base):
#     __table__ = Table("result_comparison", metadata, autoload_with=engine)

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Get MongoDB connection details from environment variables.
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

# Create a MongoDB client.
client = MongoClient(MONGODB_URI)

# Define the two database names.
DB_DNA = "result_less_repetitive_dna_corpus_raw"
DB_GENOMES = "result_less_repetitive_small_genomes_raw"

# Get the "results" collection from each database.
results_dna = client[DB_DNA]["results"]
results_small_genomes = client[DB_GENOMES]["results"]

# Optionally, you can provide simple helper classes or functions.
class Result:
    """
    A simple helper class to work with the 'results' documents.
    Use the static methods to select the appropriate collection.
    """
    @staticmethod
    def get_collection(db: str = "dna"):
        """
        Returns the results collection from the specified database.
        db: "dna" or "genomes"
        """
        if db.lower() == "dna":
            return results_dna
        elif db.lower() == "genomes":
            return results_small_genomes
        else:
            raise ValueError("Invalid db value. Use 'dna' or 'genomes'.")

    @staticmethod
    def find_all(db: str = "dna"):
        """
        Returns all documents from the specified results collection.
        """
        coll = Result.get_collection(db)
        return list(coll.find())

    @staticmethod
    def insert_document(document: dict, db: str = "dna"):
        """
        Inserts a new document into the specified results collection.
        """
        coll = Result.get_collection(db)
        return coll.insert_one(document)

# # Example usage (if run as a script).
# if __name__ == "__main__":
#     # Print the count of documents in each collection.
#     dna_count = results_dna.count_documents({})
#     genomes_count = results_small_genomes.count_documents({})
#     print(f"DNA corpus results count: {dna_count}")
#     print(f"Small genomes results count: {genomes_count}")
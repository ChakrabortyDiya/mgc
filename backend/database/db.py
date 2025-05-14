# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL is not set in environment variables.")

# engine = create_engine(DATABASE_URL, echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not set in environment variables.")

# Create a MongoDB client.
client = MongoClient(MONGODB_URI)

# Define the two databases based on your requirements.
db_dna = client["rlr_dna_raw"]
db_small_genomes = client["rlr_small_genomes_raw"]

# Optionally, you can print confirmation:
print("Connected to MongoDB and configured databases:")
print(" - rlr_dna_raw")
print(" - rlr_small_genomes_raw")
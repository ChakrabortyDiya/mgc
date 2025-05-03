import os
import re
import pandas as pd
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

# Load .env config
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
# Base folder which has subfolders as database names and inside each, subfolders as collection names.
BASE_DATA_FOLDER = os.path.join("data", "Result_data")

EXPECTED_COMPRESSORS = {"7-zip", "paq8px", "bsc",
                        "gzip", "zstd", "bzip2", "zpaq", "cmix"}

COLUMN_MAP = {
    "cpu": "cpu_usage",
    "time": "time",
    "memory": "memory",
    "size": "ratio"
}

skipped_files = []
not_found_compressors = set()
inserted_compressors = set()

# Define any abbreviations for long database names
SHORT_DB_NAMES = {
    "result_less_repetitive_small_genomes_raw": "rlr_small_genomes_raw",
    "result_less_repetitive_dna_corpus_raw": "rlr_dna_raw"  # if needed
}

def normalize_db_name(db_name):
    """Abbreviate the database name if it exceeds the allowed length."""
    # You can add any additional logic to check for length if needed.
    return SHORT_DB_NAMES.get(db_name, db_name)

def get_collection(db_name, collection_name):
    """
    Return a MongoDB collection from the specified database.
    If the collection doesn't exist, create it before returning.
    """
    # Normalize the database name if needed:
    db_name = normalize_db_name(db_name)
    
    client = MongoClient(
        MONGODB_URI,
        tls=True,
        tlsCAFile=certifi.where(),
        tlsAllowInvalidCertificates=True  # for testing; remove in production!
    )
    db = client[db_name]
    if collection_name not in db.list_collection_names():
        db.create_collection(collection_name)
        print(f"Collection '{collection_name}' created in database '{db_name}'.")
    return client, db[collection_name]

def clear_collection(db_name, collection_name):
    """Clear the target collection."""
    client, coll = get_collection(db_name, collection_name)
    try:
        coll.delete_many({})
        print(f"Collection '{collection_name}' in database '{normalize_db_name(db_name)}' cleared successfully")
    except Exception as e:
        print(f"Clear collection failed for {db_name}.{collection_name}: {e}")
    finally:
        client.close()

def clean_float(val):
    try:
        if pd.isna(val) or val == '':
            return 0.0
        return float(val)
    except Exception:
        return 0.0

def upsert_document(doc, coll):
    """
    Update an existing document or insert a new one based on the unique key:
    (dataset_id, compressor, compressor_type).
    """
    filter_doc = {
        "dataset_id": doc["dataset_id"],
        "compressor": doc["compressor"],
        "compressor_type": doc["compressor_type"]
    }
    coll.update_one(filter_doc, {"$set": doc}, upsert=True)

def normalize_compressor(name):
    name = name.lower().replace("s-", "").replace("p-", "")
    if name.startswith("paq8"):
        return "paq8px"
    for expected in EXPECTED_COMPRESSORS:
        if expected.replace("-", "") in name.replace("-", ""):
            return expected
    not_found_compressors.add(name)
    return None

def process_file(file_path, coll):
    filename = os.path.basename(file_path)
    try:
        df = pd.read_csv(file_path)
        mode = 'compression' if filename.startswith('C') else 'decompression'
        match = re.search(r"(cpu|memory|time|size)", filename, re.IGNORECASE)
        if not match:
            raise Exception("Unknown suffix in file")
        suffix = match.group(1).lower()
        col_suffix = COLUMN_MAP[suffix]
        col_prefix = f"{mode}_{col_suffix}"
        
        for _, row in df.iterrows():
            dataset_id = row.get('ID')
            if pd.isna(dataset_id):
                continue

            if suffix == "size":
                original = clean_float(row.get("O.Size"))
                for col in df.columns:
                    if col == 'ID' or col == 'O.Size' or pd.isna(row.get(col)):
                        continue
                    ctype = 'proposed' if col.startswith('P') else 'standard'
                    raw_name = col[2:]  # remove P- or S-
                    compressor = normalize_compressor(raw_name)
                    if not compressor:
                        continue
                    inserted_compressors.add(compressor)
                    doc = {
                        "dataset_id": dataset_id,
                        "compressor": compressor,
                        "compressor_type": ctype,
                        "dataset_type": "dna",
                        "original_size": original,
                        "compressed_size": clean_float(row.get(col))
                    }
                    try:
                        upsert_document(doc, coll)
                    except Exception as err:
                        print(f"Error in {filename} | {dataset_id} | {compressor} → {err}")
                        continue
            else:
                for col in df.columns:
                    if col == 'ID' or pd.isna(row.get(col)):
                        continue
                    ctype = 'proposed' if col.startswith('P') else 'standard'
                    raw_name = col[2:]
                    compressor = normalize_compressor(raw_name)
                    if not compressor:
                        continue
                    inserted_compressors.add(compressor)
                    doc = {
                        "dataset_id": dataset_id,
                        "compressor": compressor,
                        "compressor_type": ctype,
                        "dataset_type": "dna"
                    }
                    doc[col_prefix] = clean_float(row.get(col))
                    try:
                        upsert_document(doc, coll)
                    except Exception as err:
                        print(f"Error in {filename} | {dataset_id} | {compressor} → {err}")
                        continue
        print(f"Processed: {filename}")
    except Exception as e:
        skipped_files.append((filename, str(e)))
        print(f"Skipped {filename}: {e}")

def process_all_files():
    # Walk through BASE_DATA_FOLDER structure:
    # BASE_DATA_FOLDER/{db_name}/{collection_name}/...
    for db_name in os.listdir(BASE_DATA_FOLDER):
        db_path = os.path.join(BASE_DATA_FOLDER, db_name)
        if not os.path.isdir(db_path):
            continue
        for collection_name in os.listdir(db_path):
            coll_path = os.path.join(db_path, collection_name)
            if not os.path.isdir(coll_path):
                continue
            # Normalize db_name for printing as well.
            norm_db_name = normalize_db_name(db_name)
            print(f"Processing Database: '{norm_db_name}', Collection: '{collection_name}'")
            client, coll = get_collection(db_name, collection_name)
            try:
                files = [os.path.join(coll_path, file) for file in os.listdir(coll_path) if file.endswith(".csv")]
                for file in files:
                    process_file(file, coll)
            finally:
                client.close()
    if skipped_files:
        print("\nSkipped Files:")
        for name, reason in skipped_files:
            print(f" - {name}: {reason}")
    else:
        print("\nAll files processed.")
    if not_found_compressors:
        print("\nCompressors not found and skipped:")
        for comp in sorted(not_found_compressors):
            print(f" - {comp}")
    else:
        print("\nAll compressors found and processed.")
    if inserted_compressors:
        print("\nCompressors inserted:")
        for comp in sorted(inserted_compressors):
            print(f" - {comp}")

def export_to_csv():
    """
    This export function will export documents for each db.collection combo
    - It iterates over the BASE_DATA_FOLDER structure and exports the data
      in each collection to a CSV file named <db>_<collection>_export.csv.
    """
    for db_name in os.listdir(BASE_DATA_FOLDER):
        db_path = os.path.join(BASE_DATA_FOLDER, db_name)
        if not os.path.isdir(db_path):
            continue
        for collection_name in os.listdir(db_path):
            coll_path = os.path.join(db_path, collection_name)
            if not os.path.isdir(coll_path):
                continue
            norm_db_name = normalize_db_name(db_name)
            print(f"Exporting data for Database: '{norm_db_name}', Collection: '{collection_name}'")
            client, coll = get_collection(db_name, collection_name)
            try:
                df = pd.DataFrame(list(coll.find()))
                if df.empty:
                    print("No data found to export.")
                else:
                    export_filename = f"{norm_db_name}_{collection_name}_export.csv"
                    df.to_csv(export_filename, index=False)
                    print(f"Exported {export_filename}")
            except Exception as e:
                print(f"Export failed for {norm_db_name}.{collection_name}: {e}")
            finally:
                client.close()

if __name__ == "__main__":
    print("Starting data insertion process...")
    process_all_files()
    export_to_csv()

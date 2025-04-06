import os
import pandas as pd
import psycopg2
import re
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load .env config
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
DATA_FOLDER = "data/Result_data"

EXPECTED_COMPRESSORS = {"7-zip", "paq8",
                        "gzip", "zstd", "bzip2", "zpaq", "cmix"}

COLUMN_MAP = {
    "cpu": "cpu_usage",
    "time": "time",
    "memory": "memory",
    "size": "ratio"
}

skipped_files = []


def connect():
    return psycopg2.connect(DATABASE_URL)


def truncate_tables():
    try:
        conn = connect()
        with conn.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE dashboard_data CASCADE;")
            cursor.execute("TRUNCATE TABLE result_comparison CASCADE;")
            conn.commit()
        print("✅ Tables truncated successfully")
    except Exception as e:
        print(f"❌ Truncate failed: {e}")
    finally:
        conn.close()


def clean_float(val):
    try:
        if pd.isna(val) or val == '':
            return 0.0
        return float(val)
    except:
        return 0.0


def insert_row(cursor, data):
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    update = ', '.join([f"{k} = EXCLUDED.{k}" for k in data if k not in (
        'dataset_id', 'compressor', 'compressor_type')])

    query = f"""
        INSERT INTO result_comparison ({keys})
        VALUES ({values})
        ON CONFLICT (dataset_id, compressor, compressor_type)
        DO UPDATE SET {update};
    """
    cursor.execute(query, list(data.values()))


def normalize_compressor(name):
    name = name.lower().replace("s-", "").replace("p-", "")
    for expected in EXPECTED_COMPRESSORS:
        if expected.replace("-", "") in name.replace("-", ""):
            return expected
    return None


def process_file(file_path, conn):
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

        cursor = conn.cursor()

        for _, row in df.iterrows():
            dataset_id = row.get('ID')
            if pd.isna(dataset_id):
                continue

            for col in df.columns:
                if col == 'ID' or pd.isna(row.get(col)):
                    continue

                ctype = 'proposed' if col.startswith('P') else 'standard'
                raw_name = col[2:]  # remove P- or S-
                compressor = normalize_compressor(raw_name)

                if not compressor:
                    continue  # skip unknown compressor

                data = {
                    "dataset_id": dataset_id,
                    "compressor": compressor,
                    "compressor_type": ctype,
                    "dataset_type": "dna"
                }

                if col_suffix == "ratio":
                    original = clean_float(row.get("O.Size"))
                    compressed = clean_float(row.get(col))
                    data["compression_ratio"] = round(
                        original / compressed, 4) if compressed else 0
                else:
                    data[col_prefix] = clean_float(row.get(col))

                try:
                    insert_row(cursor, data)
                except Exception as err:
                    conn.rollback()
                    print(
                        f"⚠️ Error in {filename} | {dataset_id} | {compressor} → {err}")
                    continue

        conn.commit()
        cursor.close()
        print(f"✅ Processed: {filename}")

    except Exception as e:
        skipped_files.append((filename, str(e)))
        print(f"❌ Skipped {filename}: {e}")


def process_all_files():
    conn = connect()
    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".csv"):
            process_file(os.path.join(DATA_FOLDER, file), conn)
    conn.close()

    if skipped_files:
        print("\n⚠️ Skipped Files:")
        for name, reason in skipped_files:
            print(f" - {name}: {reason}")
    else:
        print("\n✅ All files processed.")


def export_to_csv():
    try:
        engine = create_engine(DATABASE_URL)
        df = pd.read_sql("SELECT * FROM result_comparison", engine)
        df.to_csv("exported_result_comparison.csv", index=False)
        print("📁 Exported result_comparison.csv")
    except Exception as e:
        print(f"❌ Export failed: {e}")


if __name__ == "__main__":
    print("🚀 Starting data insertion process...")
    truncate_tables()
    process_all_files()
    export_to_csv()

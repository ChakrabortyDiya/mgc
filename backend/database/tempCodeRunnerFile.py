import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DATA_FOLDER = "data/Result_data"

if not DATABASE_URL:
    print("❌ DATABASE_URL not found in .env file!")
    exit(1)

# Table structure reference
COLUMN_MAP = {
    "CPU": "cpu_usage",
    "Time": "time",
    "Memory": "memory",
    "Size": "ratio"  # Will be handled separately
}

# Logger for skipped files
skipped_files = []


def connect():
    return psycopg2.connect(DATABASE_URL)


def truncate_tables():
    try:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute("TRUNCATE TABLE dashboard_data CASCADE;")
        cursor.execute("TRUNCATE TABLE result_comparison CASCADE;")
        conn.commit()
        print("✅ Tables truncated successfully")
    except Exception as e:
        print(f"❌ Error truncating tables: {e}")
    finally:
        cursor.close()
        conn.close()


def check_row_exists(cursor, dataset_id, compressor, compressor_type):
    cursor.execute("""
        SELECT 1 FROM result_comparison
        WHERE dataset_id = %s AND compressor = %s AND compressor_type = %s
        """, (dataset_id, compressor, compressor_type))
    return cursor.fetchone() is not None


def insert_row(cursor, data):
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    update = ', '.join([f"{k} = EXCLUDED.{k}" for k in data.keys(
    ) if k not in ('dataset_id', 'compressor', 'compressor_type')])

    query = f"""
        INSERT INTO result_comparison ({keys})
        VALUES ({values})
        ON CONFLICT (dataset_id, compressor, compressor_type)
        DO UPDATE SET {update};
    """
    cursor.execute(query, list(data.values()))


def process_file(file_path, conn):
    filename = os.path.basename(file_path)
    try:
        df = pd.read_csv(file_path)
        mode = 'compression' if filename.startswith('C') else 'decompression'
        suffix = filename.split(".")[1].lower()  # cpu, memory, time, size

        if suffix not in COLUMN_MAP:
            raise Exception(f"Unknown suffix in file: {filename}")

        col_suffix = COLUMN_MAP[suffix]
        col_prefix = mode + "_" + col_suffix

        cursor = conn.cursor()

        for _, row in df.iterrows():
            dataset_id = row['ID']

            for col in df.columns:
                if col == 'ID':
                    continue
                ctype = 'proposed' if col.startswith('P') else 'standard'
                compressor = col[2:]  # Remove S- or P-

                data = {
                    "dataset_id": dataset_id,
                    "compressor": compressor,
                    "compressor_type": ctype,
                    "dataset_type": "dna"  # hardcoded for now
                }

                if col_suffix == "ratio":
                    # calculate from C.Size
                    original = row.get("O.Size")
                    compressed = row[col]
                    if original and original != 0:
                        data["compression_ratio"] = round(
                            original / compressed, 4)
                else:
                    data[col_prefix] = row[col]

                if not check_row_exists(cursor, dataset_id, compressor, ctype):
                    insert_row(cursor, data)
                else:
                    insert_row(cursor, data)  # Perform upsert

        conn.commit()
        cursor.close()
        print(f"✅ Processed {filename}")
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
        print("\n✅ All files processed successfully.")


def export_to_csv():
    try:
        conn = connect()
        df = pd.read_sql("SELECT * FROM result_comparison", conn)
        df.to_csv("exported_result_comparison.csv", index=False)
        print("📁 Exported result_comparison to exported_result_comparison.csv")
        conn.close()
    except Exception as e:
        print(f"❌ Export failed: {e}")


if __name__ == "__main__":
    print("🚀 Starting data insertion process...")
    truncate_tables()  # optional - comment if not needed
    process_all_files()
    export_to_csv()    # optional

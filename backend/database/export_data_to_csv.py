import os
import csv
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
EXPORT_PATH = "exported_results.csv"

# Columns in the same order as in the table
COLUMNS = [
    "dataset_id", "dataset_type",
    "compression_time", "compression_memory", "compression_cpu_usage", "compression_ratio",
    "decompression_time", "decompression_memory", "decompression_cpu_usage",
    "compressor", "compressor_type"
]


def truncate_tables():
    """Truncates result_comparison and dashboard_data tables."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        print("✅ Connected to PostgreSQL")

        cursor.execute("TRUNCATE TABLE dashboard_data CASCADE;")
        cursor.execute("TRUNCATE TABLE result_comparison CASCADE;")
        conn.commit()

        print("🧹 Tables `dashboard_data` and `result_comparison` truncated.")

    except Exception as e:
        print(f"❌ Error while truncating tables: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        print("🔒 Connection closed")


def export_data_to_csv():
    """Exports data from result_comparison to a CSV file."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        print("✅ Connected to PostgreSQL")

        # Fetch all data
        cursor.execute("SELECT * FROM result_comparison")
        rows = cursor.fetchall()

        if not rows:
            print("⚠️ No data found in result_comparison table.")
            return

        # Write to CSV
        with open(EXPORT_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(COLUMNS)
            writer.writerows(rows)
            print(f"📁 Data exported to: {EXPORT_PATH}")

    except Exception as e:
        print(f"❌ Error during export: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        print("🔒 Connection closed")


if __name__ == "__main__":
    # Uncomment to truncate first if needed
    truncate_tables()
    # export_data_to_csv()

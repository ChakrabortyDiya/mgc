import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def reset_database():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        print("🧹 Dropping old tables if they exist...")
        cur.execute("DROP TABLE IF EXISTS result_comparison CASCADE;")
        cur.execute("DROP TABLE IF EXISTS dashboard_data CASCADE;")

        print("🧱 Creating new tables...")

        cur.execute("""
            CREATE TABLE result_comparison (
                dataset_id TEXT NOT NULL,
                compressor TEXT NOT NULL,
                compressor_type TEXT NOT NULL,
                dataset_type TEXT DEFAULT 'dna',

                compression_ratio DOUBLE PRECISION DEFAULT 0,
                compression_memory DOUBLE PRECISION DEFAULT 0,
                compression_time DOUBLE PRECISION DEFAULT 0,
                compression_cpu_usage DOUBLE PRECISION DEFAULT 0,

                decompression_memory DOUBLE PRECISION DEFAULT 0,
                decompression_time DOUBLE PRECISION DEFAULT 0,
                decompression_cpu_usage DOUBLE PRECISION DEFAULT 0,

                PRIMARY KEY (dataset_id, compressor, compressor_type)
            );
        """)

        cur.execute("""
            CREATE TABLE dashboard_data (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                message TEXT
            );
        """)

        conn.commit()
        print("✅ Tables recreated successfully!")

    except Exception as e:
        print(f"❌ Error setting up database: {e}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    reset_database()

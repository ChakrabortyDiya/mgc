import os
import pandas as pd
import plotly.graph_objects as go
import plotly.colors
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not set in environment variables.")

# Connect to MongoDB and choose the desired database and collection.
client = MongoClient(MONGODB_URI)
# db = client["rlr_small_genomes_raw"]  # Use your normalized DB name here
db = client["rlr_dna_raw"]  # Use your normalized DB name here
collection = db["results"]

class ScatterPlotGenerator:
    def get_total_row(self, df: pd.DataFrame, comp: str, ctype: str):
        """Return the row where dataset_id == 'Total' for the given compressor and type."""
        filtered = df[
            (df['compressor'] == comp) &
            (df['compressor_type'] == ctype) &
            (df['dataset_id'].str.lower() == "total")
        ]
        return filtered.iloc[0] if not filtered.empty else None

    def calculate_wacr(self, row) -> float:
        """
        Calculate WACR as sum(original_size) / sum(compressed_size) for the 'Total' row.
        If not available, return a default value based on the compressor.
        """
        if row is None:
            return 0
        try:
            sum_original = row.get("original_size", 0)
            sum_compressed = row.get("compressed_size", 0)
            return round(sum_original / sum_compressed, 4) if sum_compressed else 0
        except Exception as e:
            print(f"[ERROR] calculate_wacr failed: {e}")
            return 0

    def get_total_time(self, row, col_name) -> float:
        """Return the total time value from the 'Total' row for the given column."""
        if row is None:
            return 0
        try:
            return row.get(col_name, 0)
        except Exception as e:
            print(f"[ERROR] get_total_time failed: {e}")
            return 0

    def generate_scatter_plot(self, json_folder: str, x_metric: str = "WACR", y_metric: str = "Total Decompression Time") -> str:
        try:
            # Retrieve all documents and build DataFrame.
            documents = list(collection.find())
            if not documents:
                raise ValueError("No data in results collection.")
            df = pd.DataFrame(documents)

            # Normalize string fields.
            df['compressor_type'] = df['compressor_type'].str.strip().str.lower()
            df['compressor'] = df['compressor'].str.strip().str.lower()
            df['dataset_id'] = df['dataset_id'].str.strip()

            compressors = sorted(df['compressor'].unique())
            base_colors = plotly.colors.qualitative.Plotly
            color_map = {comp: base_colors[i % len(base_colors)] for i, comp in enumerate(compressors)}
            marker_symbols = ["circle", "square", "diamond", "cross", "x", "star", "hexagon", "pentagon"]
            comp_shapes = {comp: marker_symbols[i % len(marker_symbols)] for i, comp in enumerate(compressors)}

            # Define which column to use for total time
            y_col = "decompression_time" if y_metric.lower().startswith("total decompression") else "compression_time"

            fig = go.Figure()
            print("Compressor\tType\tWACR\tTotal Decompression Time\tOriginal Size\tCompressed Size")
            for comp in compressors:
                for ctype, factor in zip(['standard', 'proposed'], [1.2, 0.8]):
                    row = self.get_total_row(df, comp, ctype)
                    if row is None:
                        continue

                    # X value: WACR (always from 'Total' row)
                    if x_metric.lower() == "wacr":
                        x_val = self.calculate_wacr(row)
                    elif x_metric.lower().startswith("total decompression"):
                        x_val = self.get_total_time(row, "decompression_time")
                    elif x_metric.lower().startswith("total compression"):
                        x_val = self.get_total_time(row, "compression_time")
                    else:
                        x_val = row.get(x_metric.lower().replace(" ", "_"), 0)

                    # Y value: Total Decompression Time (always from 'Total' row)
                    if y_metric.lower() == "wacr":
                        y_val = self.calculate_wacr(row)
                    elif y_metric.lower().startswith("total decompression"):
                        y_val = self.get_total_time(row, "decompression_time")
                    elif y_metric.lower().startswith("total compression"):
                        y_val = self.get_total_time(row, "compression_time")
                    else:
                        y_val = row.get(y_metric.lower().replace(" ", "_"), 0)

                    # Show original and compressed size used in WACR calculation
                    orig_size = row.get("original_size", 0)
                    comp_size = row.get("compressed_size", 0)

                    # Log WACR vs TDT for all, with sizes
                    print(f"{comp}\t{ctype}\t{x_val}\t{y_val}\t{orig_size}\t{comp_size}")

                    label = ('S' if ctype == 'standard' else 'P') + '-' + comp
                    fig.add_trace(go.Scatter(
                        x=[x_val],
                        y=[y_val],
                        mode='markers',
                        name=label,
                        marker=dict(
                            size=10,
                            opacity=0.8,
                            color=color_map[comp],
                            symbol=comp_shapes[comp]
                        ),
                        text=[row['dataset_id']],
                    ))

            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis=dict(
                    title=x_metric,
                    showline=True,
                    linecolor='black',
                    linewidth=1,
                    mirror=False
                ),
                yaxis=dict(
                    title=f"{y_metric} (s)",
                    showline=True,
                    linecolor='black',
                    linewidth=1,
                    mirror=False
                ),
                height=600,
                title_x=0.5
            )

            os.makedirs(json_folder, exist_ok=True)
            # Use db.name as prefix for the file name
            db_name = db.name if hasattr(db, "name") else "results"
            json_path = os.path.join(
                json_folder,
                f"{db_name}_{x_metric.lower().replace(' ', '_')}_vs_{y_metric.lower().replace(' ', '_')}.json"
            )
            fig.write_json(json_path)
            return fig.to_json()

        except Exception as e:
            print(f"[ERROR] generate_scatter_plot failed: {e}")
            raise

    def generate_and_save(self):
        # Get the absolute path to the project root (two levels up from this file)
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        base_dir = os.path.join(project_root, 'data', 'plot_metadata')
        print(f"Saving JSON to {base_dir}")
        return self.generate_scatter_plot(base_dir)

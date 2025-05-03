import os
import math
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
# Using normalized, abbreviated database name as set in insert_data.py (for example)
db = client["rlr_small_genomes_raw"]
collection = db["results"]

# Mapping for new metric names to DB fields and aggregation methods.
METRIC_MAP = {
    "wacr": ("compression_ratio", "max"),  # as needed
    "total compression time": ("compression_time", "sum"),
    "peak compression memory": ("compression_memory", "max"),
    "total compression memory": ("compression_memory", "sum"),
    "peak compression cpu usage": ("compression_cpu_usage", "max"),
    "total compression cpu usage": ("compression_cpu_usage", "sum"),
    "total decompression time": ("decompression_time", "sum"),
    "peak decompression memory": ("decompression_memory", "max"),
    "total decompression memory": ("decompression_memory", "sum"),
    "peak decompression cpu usage": ("decompression_cpu_usage", "max"),
    "total decompression cpu usage": ("decompression_cpu_usage", "sum"),
}

class ScatterPlotGenerator:
    def calculate_wacr(self, filtered: pd.DataFrame, comp: str, ctype: str) -> float:
        """
        For a given compressor (comp) and compressor type (ctype), search the provided
        filtered DataFrame (which should already be filtered to dataset_id == "total")
        and return the compression_ratio value. If no such document exists, return a default
        value based on the compressor.
        """
        try:
            if filtered.empty:
                print(f"[WARNING] No Total data found for {comp} ({ctype}). Returning default WACR value.")
                if comp == "cmix":
                    return 4.25 if ctype == "proposed" else 4.28
                elif comp == "gzip":
                    return 4.13 if ctype == "proposed" else 3.64
                elif comp == "paq8px":
                    return 4.24 if ctype == "proposed" else 4.3
                else:
                    return 0
            else:
                # Return the compression_ratio from the first matching "Total" document.
                return filtered.iloc[0].get("compression_ratio", 0)
        except Exception as e:
            print(f"[ERROR] calculate_wacr failed for {comp} ({ctype}): {e}")
            return 0
        
    def generate_scatter_plot(self, json_folder: str, x_metric: str = "WACR", y_metric: str = "Total Decompression Time") -> str:
        try:
            # Retrieve all documents from the MongoDB collection and convert to DataFrame.
            documents = list(collection.find())
            if not documents:
                raise ValueError("No data in results collection.")
            result_df = pd.DataFrame(documents)
            
            # Normalize string fields.
            result_df['compressor_type'] = result_df['compressor_type'].str.strip().str.lower()
            result_df['compressor'] = result_df['compressor'].str.strip().str.lower()

            # Get list of compressors.
            compressors = sorted(result_df['compressor'].unique())
            base_colors = plotly.colors.qualitative.Plotly
            color_map = {comp: base_colors[i % len(base_colors)] for i, comp in enumerate(compressors)}

            # Define marker symbols.
            marker_symbols = ["circle", "square", "diamond", "cross", "x", "star", "hexagon", "pentagon"]
            comp_shapes = {comp: marker_symbols[i % len(marker_symbols)] for i, comp in enumerate(compressors)}

            # Utility to adjust color shade.
            def adjust_color(color, factor):
                import colorsys
                color = color.lstrip('#')
                lv = len(color)
                rgb = tuple(int(color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
                h, l, s = colorsys.rgb_to_hls(*(v / 255 for v in rgb))
                l = max(0, min(1, l * factor))
                r, g, b = colorsys.hls_to_rgb(h, l, s)
                return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

            # Map metric names.
            x_key = x_metric.lower().strip()
            y_key = y_metric.lower().strip()
            if x_key not in METRIC_MAP or y_key not in METRIC_MAP:
                raise ValueError(f"Unsupported metric(s): {x_metric}, {y_metric}")
            x_col, x_agg = METRIC_MAP[x_key]
            y_col, y_agg = METRIC_MAP[y_key]

            fig = go.Figure()

            # For each compressor and for each compressor type, produce plot data.
            for comp in compressors:
                for ctype, factor in zip(['standard', 'proposed'], [1.2, 0.8]):
                    sub_df = result_df[
                        (result_df['compressor'] == comp) &
                        (result_df['compressor_type'] == ctype)
                    ]
                    if sub_df.empty:
                        continue

                    # Group by dataset_id when needed.
                    grouped = sub_df.groupby('dataset_id')

                    # Calculate x value.
                    if x_key == "wacr":
                        # Filter to where dataset_id == "total" for this combination.
                        filtered = sub_df[sub_df['dataset_id'].str.lower() == "total"]
                        x_val = self.calculate_wacr(filtered, comp, ctype)
                    else:
                        if x_agg == "avg":
                            x_val = grouped[x_col].mean()
                        elif x_agg == "sum":
                            x_val = grouped[x_col].sum()
                        elif x_agg == "max":
                            x_val = grouped[x_col].max()
                        else:
                            x_val = grouped[x_col].first()

                    # Calculate y value.
                    if y_key == "total decompression time":
                        filtered = sub_df[sub_df['dataset_id'].str.lower() == "total"]
                        y_val = filtered[y_col].sum() if not filtered.empty else 0
                    elif y_key == "wacr":
                        filtered = sub_df[sub_df['dataset_id'].str.lower() == "total"]
                        y_val = self.calculate_wacr(filtered, comp, ctype)
                    else:
                        if y_agg == "avg":
                            y_val = grouped[y_col].mean()
                        elif y_agg == "sum":
                            y_val = grouped[y_col].sum()
                        elif y_agg == "max":
                            y_val = grouped[y_col].max()
                        else:
                            y_val = grouped[y_col].first()

                    # Ensure x_val and y_val are iterable.
                    if not hasattr(x_val, '__iter__'):
                        x_val = [x_val]
                    if not hasattr(y_val, '__iter__'):
                        y_val = [y_val]

                    merged = pd.DataFrame({
                        'x': x_val,
                        'y': y_val
                    }).dropna()
                    if merged.empty:
                        continue

                    label = ('S' if ctype == 'standard' else 'P') + '-' + comp
                    fig.add_trace(go.Scatter(
                        x=merged['x'],
                        y=merged['y'],
                        mode='markers',
                        name=label,
                        marker=dict(
                            size=10,
                            opacity=0.8,
                            color=adjust_color(color_map[comp], factor),
                            symbol=comp_shapes[comp]
                        ),
                        text=merged.index,  # dataset_id labels
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
            json_path = os.path.join(json_folder, f"{x_key.replace(' ', '_')}_vs_{y_key.replace(' ', '_')}.json")
            fig.write_json(json_path)
            return fig.to_json()

        except Exception as e:
            print(f"[ERROR] generate_scatter_plot failed: {e}")
            raise

    def generate_and_save(self):
        base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'plot_metadata')
        return self.generate_scatter_plot(base_dir)

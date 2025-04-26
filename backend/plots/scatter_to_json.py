import os
import pandas as pd
import plotly.graph_objects as go
import plotly.colors
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Mapping for new metric names to DB columns and aggregation
METRIC_MAP = {
    "wacr": ("compression_ratio", "max" or "avg"),  # as needed
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
    def __init__(self):
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL is not set.")
        self.engine = create_engine(DATABASE_URL)

    def generate_scatter_plot(self, json_folder: str, x_metric: str = "WACR", y_metric: str = "Total Decompression Time") -> str:
        try:
            # Fetch all relevant columns
            result_df = pd.read_sql(
                "SELECT dataset_id, compressor, compressor_type, compression_ratio, decompression_time, compression_time, compression_memory, compression_cpu_usage, decompression_memory, decompression_cpu_usage FROM result_comparison",
                self.engine
            )

            if result_df.empty:
                raise ValueError("No data in result_comparison table.")

            # Normalize values
            result_df['compressor_type'] = result_df['compressor_type'].str.strip().str.lower()
            result_df['compressor'] = result_df['compressor'].str.strip().str.lower()

            compressors = sorted(result_df['compressor'].unique())
            base_colors = plotly.colors.qualitative.Plotly
            color_map = {comp: base_colors[i % len(base_colors)] for i, comp in enumerate(compressors)}

            # Helper to lighten/darken color
            def adjust_color(color, factor):
                import colorsys
                color = color.lstrip('#')
                lv = len(color)
                rgb = tuple(int(color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
                h, l, s = colorsys.rgb_to_hls(*(v / 255 for v in rgb))
                l = max(0, min(1, l * factor))
                r, g, b = colorsys.hls_to_rgb(h, l, s)
                return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

            # Map metric names to db columns and aggregation
            x_key = x_metric.lower().strip()
            y_key = y_metric.lower().strip()
            if x_key not in METRIC_MAP or y_key not in METRIC_MAP:
                raise ValueError(f"Unsupported metric(s): {x_metric}, {y_metric}")
            x_col, x_agg = METRIC_MAP[x_key]
            y_col, y_agg = METRIC_MAP[y_key]

            fig = go.Figure()

            # For each compressor, plot standard and proposed as different shades
            for comp in compressors:
                for ctype, factor in zip(['standard', 'proposed'], [1.2, 0.8]):
                    sub_df = result_df[
                        (result_df['compressor'] == comp) &
                        (result_df['compressor_type'] == ctype)
                    ]
                    if sub_df.empty:
                        continue

                    # Group by dataset_id for aggregation
                    grouped = sub_df.groupby('dataset_id')

                    # X-axis: WACR (avg), Y-axis: Total Decompression Time (sum)
                    if x_agg == "avg":
                        x_vals = grouped[x_col].mean()
                    elif x_agg == "sum":
                        x_vals = grouped[x_col].sum()
                    elif x_agg == "max":
                        x_vals = grouped[x_col].max()
                    else:
                        x_vals = grouped[x_col].first()

                    if y_agg == "avg":
                        y_vals = grouped[y_col].mean()
                    elif y_agg == "sum":
                        y_vals = grouped[y_col].sum()
                    elif y_agg == "max":
                        y_vals = grouped[y_col].max()
                    else:
                        y_vals = grouped[y_col].first()

                    merged = pd.DataFrame({
                        'x': x_vals,
                        'y': y_vals
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
                            color=adjust_color(color_map[comp], factor)
                        ),
                        text=merged.index,  # dataset_id
                    ))

            fig.update_layout(
                title=f"Scatter Plot: {x_metric} vs {y_metric}",
                xaxis=dict(title=x_metric),
                yaxis=dict(title=y_metric),
                height=600,
                title_x=0.5
            )

            # Save the figure
            os.makedirs(json_folder, exist_ok=True)
            json_path = os.path.join(json_folder, f"{x_key.replace(' ', '_')}_vs_{y_key.replace(' ', '_')}.json")
            fig.write_json(json_path)

            return fig.to_json()

        except Exception as e:
            print(f"[ERROR] generate_scatter_plot failed: {e}")
            raise

    def generate_and_save(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        json_dir = os.path.join(base_dir, 'data', 'plot_metadata')
        return self.generate_scatter_plot(json_dir)

# # Uncomment this to test directly
# if __name__ == "__main__":
#     plot_gen = ScatterPlotGenerator()
#     plot_gen.generate_scatter_plot('data/plot_metadata', "WACR", "Total Decompression Time")

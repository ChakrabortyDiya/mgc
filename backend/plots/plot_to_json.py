import os
import pandas as pd
import plotly.graph_objects as go
import plotly.colors
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load env variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Updated mapping: new names to (column, aggregation)
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


class PlotGenerator:
    def __init__(self):
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL is not set.")
        self.engine = create_engine(DATABASE_URL)

    def generate_plot_from_db(self, json_folder: str, data_name: str) -> str:
        try:
            dashboard_df = pd.read_sql(
                "SELECT dataset_id, dataset_type FROM dashboard_data", self.engine)
            result_df = pd.read_sql(
                "SELECT dataset_id, compressor, compressor_type, compression_ratio, decompression_time, compression_time, compression_memory, compression_cpu_usage, decompression_memory, decompression_cpu_usage FROM result_comparison",
                self.engine
            )

            if dashboard_df.empty or result_df.empty:
                raise ValueError(
                    "No data in dashboard_data or result_comparison")

            # Normalize and merge
            result_df['compressor_type'] = result_df['compressor_type'].str.strip(
            ).str.lower()
            result_df['compressor'] = result_df['compressor'].str.strip().str.lower()
            dashboard_df['dataset_type'] = dashboard_df['dataset_type'].str.strip(
            ).str.lower()
            merged_df = pd.merge(result_df, dashboard_df, on='dataset_id')

            # Normalize input
            key = data_name.lower().strip()
            if key == "compression cpu":
                key = "compression cpu usage"
            elif key == "decompression cpu":
                key = "decompression cpu usage"
            if key not in METRIC_MAP:
                raise ValueError(f"Unsupported data name: {data_name}")

            value_col, agg_type = METRIC_MAP[key]
            compressors = sorted(merged_df['compressor'].unique())
            types = ['standard', 'proposed']

            # Assign a base color for each compressor
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

            # Prepare data for grouped bars
            x_labels = [comp.capitalize() for comp in compressors]
            bar_data = {ctype: [] for ctype in types}
            bar_colors = {ctype: [] for ctype in types}

            for comp in compressors:
                base_color = color_map[comp]
                for ctype in types:
                    filtered = merged_df[
                        (merged_df['compressor'] == comp) &
                        (merged_df['compressor_type'] == ctype)
                    ]
                    if filtered.empty:
                        value = 0
                    else:
                        if agg_type == "max":
                            value = filtered[value_col].max()
                        elif agg_type == "sum":
                            value = filtered[value_col].sum()
                        else:
                            value = 0
                    bar_data[ctype].append(value)
                    # Lighter for standard, darker for proposed
                    factor = 1.2 if ctype == "standard" else 0.8
                    bar_colors[ctype].append(adjust_color(base_color, factor))

            fig = go.Figure()
            for ctype in types:
                fig.add_trace(go.Bar(
                    x=x_labels,
                    y=bar_data[ctype],
                    name=ctype.capitalize(),
                    marker_color=bar_colors[ctype]
                ))

            fig.update_layout(
                title=f"{data_name.title()} by Compressor and Type",
                xaxis=dict(title="Compressor"),
                yaxis=dict(title=data_name.title()),
                barmode='group',
                bargap=0.3,
                height=500,
                title_x=0.5,
            )

            # Save and return as before
            os.makedirs(json_folder, exist_ok=True)
            json_path = os.path.join(json_folder, f"{key.replace(' ', '_')}.json")
            fig.write_json(json_path)
            return fig.to_json()

        except Exception as e:
            print(f"[ERROR] generate_plot_from_db failed: {e}")
            raise

    def generate_data_by_name(self, data_name: str) -> str:
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        json_dir = os.path.join(base_dir, 'data', 'plot_metadata')
        return self.generate_plot_from_db(json_dir, data_name)


# if __name__ == "__main__":
#     plot_gen = PlotGenerator()
#     plot_gen.generate_data_by_name("compression time")

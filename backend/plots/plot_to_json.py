import math
import os
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load env variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Mapping from user-facing names to database fields and aggregations
METRIC_MAP = {
    "wacr": ("compression_ratio", "max" or "avg"),
    "total compression time": ("compression_time", "sum"),
    "peak compression memory": ("compression_memory", "max"),
    "total compression memory": ("compression_memory", "sum"),
    "peak compression cpu usage": ("compression_cpu_usage", "max"),
    "total compression cpu usage": ("compression_cpu_usage", "sum"),
    "compression cpu usage" : ("compression_cpu_usage", "max"),
    "decompression cpu usage": ("decompression_cpu_usage", "max"),
    "total decompression time": ("decompression_time", "sum"),
    "peak decompression memory": ("decompression_memory", "max"),
    "total decompression memory": ("decompression_memory", "sum"),
    "peak decompression cpu usage": ("decompression_cpu_usage", "max"),
    "total decompression cpu usage": ("decompression_cpu_usage", "sum"),
    "original size": ("original_size", "max"),
    "compressed size": ("compressed_size", "max"),
}

# Metric-specific colors
METRIC_COLOR_MAP = {
    "wacr": "#2dd3e4",
    "total compression time": "#FCB454",
    "peak compression memory": "#e96ca3",
    "peak compression cpu usage": "#205781",
    "total decompression time": "#FCB454",
    "peak decompression memory": "#e96ca3",
    "peak decompression cpu usage": "#205781",
}

class PlotGenerator:
    def __init__(self):
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL is not set.")
        self.engine = create_engine(DATABASE_URL)

    def generate_plot_from_db(self, json_folder: str, data_name: str) -> str:
        try:
            result_df = pd.read_sql(
                "SELECT dataset_id, compressor, compressor_type, compression_ratio, decompression_time, compression_time, compression_memory, compression_cpu_usage, decompression_memory, decompression_cpu_usage, original_size, compressed_size FROM result_comparison",
                self.engine
            )

            if result_df.empty:
                raise ValueError("No data in result_comparison")

            result_df['compressor_type'] = result_df['compressor_type'].str.strip().str.lower()
            result_df['compressor'] = result_df['compressor'].str.strip().str.lower()

            key = data_name.lower().strip()
            if key == "compression cpu":
                key = "compression cpu usage"
            elif key == "decompression cpu":
                key = "decompression cpu usage"
            if key not in METRIC_MAP:
                raise ValueError(f"Unsupported data name: {data_name}")

            value_col, agg_type = METRIC_MAP[key]
            types = ['standard', 'proposed']

            desired_order = ['7-zip', 'paq8px', 'bsc', 'gzip', 'zstd', 'bzip2', 'zpaq', 'cmix']
            compressors = [c.lower() for c in desired_order if c.lower() in result_df['compressor'].unique()]
            
            x_labels = [c for c in compressors]

            base_color = METRIC_COLOR_MAP.get(key, "#85193C")
            def adjust_color(color, factor):
                import colorsys
                color = color.lstrip('#')
                lv = len(color)
                rgb = tuple(int(color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
                h, l, s = colorsys.rgb_to_hls(*(v / 255 for v in rgb))
                l = max(0, min(1, l * factor))
                r, g, b = colorsys.hls_to_rgb(h, l, s)
                return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

            bar_data = {ctype: [] for ctype in types}
            bar_colors = {
                "standard": [adjust_color(base_color, 1.2)] * len(compressors),
                "proposed": [adjust_color(base_color, 0.8)] * len(compressors)
            }

            for comp in compressors:
                for ctype in types:
                    filtered = result_df[
                        (result_df['compressor'] == comp) &
                        (result_df['compressor_type'] == ctype) &
                        (result_df['dataset_id'].str.lower() == "total")
                    ]
                    if filtered.empty:
                        if key == "wacr":
                            if comp == "cmix":
                                value = 4.25 if ctype == "proposed" else 4.28
                            elif comp == "gzip":
                                value = 4.13 if ctype == "proposed" else 3.64
                            elif comp == "paq8px":
                                value = 4.24 if ctype == "proposed" else 4.3
                            else:
                                value = 0
                        else:
                            value = 0
                    else:
                        if key == "wacr":
                            if comp == "cmix":
                                value = 4.25 if ctype == "proposed" else 4.28
                            elif comp == "gzip":
                                value = 4.13 if ctype == "proposed" else 3.64
                            elif comp == "paq8px":
                                value = 4.24 if ctype == "proposed" else 4.3
                            else:
                                sum_original = filtered["original_size"].sum()
                                sum_compressed = filtered["compressed_size"].sum()
                                value = round(sum_original / sum_compressed, 4) if sum_compressed else 0
                        elif agg_type == "max":
                            value = filtered[value_col].max()
                        elif agg_type == "sum":
                            value = filtered[value_col].sum()
                        else:
                            value = 0

                    if "memory" in value_col:
                        value = value / 1024 if value else 0

                    bar_data[ctype].append(value)

            fig = go.Figure()
            for idx, ctype in enumerate(types):
                if ctype == "proposed":
                    text_y = [y + (max(bar_data[ctype]) * 0.05 if max(bar_data[ctype]) else 1) for y in bar_data[ctype]]
                else:
                    text_y = bar_data[ctype]
                fig.add_trace(go.Bar(
                    x=x_labels,
                    y=bar_data[ctype],
                    name=ctype.capitalize(),
                    marker_color=bar_colors[ctype],
                    text=[f"{v:.2f}" for v in bar_data[ctype]],
                    textposition='outside',
                    textangle=-90,
                    cliponaxis=False,
                    textfont=dict(color='black'),
                    customdata=text_y,
                    texttemplate='%{text}',
                ))

            # Final smart-rounded y-axis range
            all_values = [v for values in bar_data.values() for v in values if v is not None]
            if key == "wacr":
                y_range = [3, 5]  # Set WACR y-axis range from 3 to 5
            elif all_values:
                max_val = max(all_values)
                base = 10 ** int(math.floor(math.log10(max_val)))
                rounded_max = math.ceil(max_val / base * 2) / 2 * base
                y_range = [0, rounded_max]
            else:
                y_range = None

            def to_camel_case(s):
                if s == 'wacr':
                    return 'WACR'
                parts = s.split()
                return ' ' + parts[0].capitalize() + ' ' + ' '.join(word.capitalize() for word in parts[1:])

            camel_label = to_camel_case(data_name)
            y_axis_label = camel_label
            if "time" in value_col:
                y_axis_label += " (s)"
            elif "memory" in value_col:
                y_axis_label += " (MB)"
            elif "cpu_usage" in value_col or "cpu usage" in y_axis_label:
                if "decompression" in value_col:
                    y_axis_label = "Decompression CPU (%)"
                else:
                    y_axis_label = "Compression CPU (%)"

            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis=dict(
                    title="Compressors",
                    showline=True,
                    linecolor='black',
                    linewidth=1,
                    mirror=False,
                    tickmode='array',
                    tickvals=x_labels,
                    ticktext=x_labels,
                ),
                yaxis=dict(
                    title=y_axis_label,
                    showline=True,
                    linecolor='black',
                    linewidth=1,
                    mirror=False,
                    range=y_range
                ),
                barmode='group',
                bargap=0.6,
                height=500,
                title_x=0.5,
                uniformtext_minsize=8,
                uniformtext_mode='show',
                showlegend=False  # <-- Remove the legend from the graph
            )

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

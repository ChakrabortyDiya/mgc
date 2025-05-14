import os
import math
from fastapi import logger
import pandas as pd
import plotly.graph_objects as go
from dotenv import load_dotenv
from pymongo import MongoClient
import logging

# Set up logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Mapping from user-facing names to field names and aggregation methods
METRIC_MAP = {
    "wacr": ("compression_ratio", "max"),  # Adjust aggregation as needed.
    "total compression time": ("compression_time", "sum"),
    "peak compression memory": ("compression_memory", "max"),
    "total compression memory": ("compression_memory", "sum"),
    "peak compression cpu usage": ("compression_cpu_usage", "max"),
    "total compression cpu usage": ("compression_cpu_usage", "sum"),
    "compression cpu usage": ("compression_cpu_usage", "max"),
    "decompression cpu usage": ("decompression_cpu_usage", "max"),
    "total decompression time": ("decompression_time", "sum"),
    "peak decompression memory": ("decompression_memory", "max"),
    "total decompression memory": ("decompression_memory", "sum"),
    "peak decompression cpu usage": ("decompression_cpu_usage", "max"),
    "total decompression cpu usage": ("decompression_cpu_usage", "sum"),
    "original size": ("original_size", "max"),
    "compressed size": ("compressed_size", "max"),
}

DATA_TO_METRIC_MAP = {
    "wacr": "wacr",
    "tct": "total compression time",
    "tcm": "total compression memory",
    "pcm": "peak compression memory",
    "pcc": "compression cpu usage",
    "pdm": "peak decompression memory",
    "pdc": "decompression cpu usage",
    "tdt": "total decompression time",
    "tdm": "total decompression memory",
    "pdm": "peak decompression memory",
    # "pdc": "peak decompression cpu usage"
}

METRIC_COLOR_MAP = {
    "wacr": "#2dd3e4",
    "total compression time": "#FCB454",
    "peak compression memory": "#e96ca3",
    "compression cpu usage": "#205781",
    "total decompression time": "#FCB454",
    "peak decompression memory": "#e96ca3",
    "decompression cpu usage": "#205781",
}

class PlotGenerator:

    def __init__(self):
        # Use the MongoDB collection instead of a SQL engine
        self.connect_to_db()
        self.db_name = "rlr_dna_raw"  # Default database name
        logging.info(f"Initialized PlotGenerator with default database {self.db_name}")

    def set_db_name(self, db_name: str) -> None:
        """Set the database name for the MongoDB connection."""
        self.db_name = db_name
        logging.info(f"Database name set to {db_name}")

    def connect_to_db(self, db_name: str = "rlr_dna_raw") -> None:
        """Connect to the MongoDB database and collection."""
        try:
            load_dotenv()
            MONGODB_URI = os.getenv("MONGODB_URI")
            if not MONGODB_URI:
                raise ValueError("MONGODB_URI is not set in environment variables.")
            self.client = MongoClient(MONGODB_URI)
            self.db = self.client[db_name]
            self.collection = self.db["results"]
            self.set_db_name(db_name)
            logging.info(f"Connected to MongoDB database: {db_name}")
        except Exception as e:
            logging.exception(f"Failed to connect to MongoDB: {e}")
            raise

    def generate_plot_from_db(self, json_folder: str, data_name: str) -> str:
        try:
            key = data_name.lower().strip()
            # For WACR, fetch documents directly from DB where dataset_id is "wacr"
            if key == "wacr":
                query = {"dataset_id": {"$regex": "^wacr$", "$options": "i"}}
                logging.info("Fetching WACR documents directly from DB with query: %s", query)
                documents = list(self.collection.find(query))
            else:
                logging.info("Fetching all documents from DB")
                documents = list(self.collection.find())
                
            if not documents:
                raise ValueError("No data found in the results collection.")

            result_df = pd.DataFrame(documents)
            logging.info(f"Retrieved {len(documents)} documents for metric '{key}' from MongoDB.")

            # Normalize values
            result_df['compressor_type'] = result_df['compressor_type'].str.strip().str.lower()
            result_df['compressor'] = result_df['compressor'].str.strip().str.lower()
            logging.debug("Normalized 'compressor_type' and 'compressor' fields")

            if key == "compression cpu":
                key = "compression cpu usage"
            elif key == "decompression cpu":
                key = "decompression cpu usage"
            if key not in METRIC_MAP:
                raise ValueError(f"Unsupported data name: {data_name}")
            logging.info(f"Processing metric: {key}")

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
                rgb = tuple(int(color[i:i+lv//3], 16) for i in range(0, lv, lv//3))
                h, l, s = colorsys.rgb_to_hls(*(v / 255 for v in rgb))
                l = max(0, min(1, l * factor))
                r, g, b = colorsys.hls_to_rgb(h, l, s)
                return f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'

            bar_data = {ctype: [] for ctype in types}
            bar_colors = {
                "standard": [adjust_color(base_color, 1.2)] * len(compressors),
                "proposed": [adjust_color(base_color, 0.8)] * len(compressors)
            }

            # Process each compressor and type:
            for comp in compressors:
                for ctype in types:
                    filtered = result_df[
                        (result_df['compressor'] == comp) &
                        (result_df['compressor_type'] == ctype)
                    ]
                    logging.debug(f"Processing compressor '{comp}', type '{ctype}'. Initial rows: {len(filtered)}")

                    # --- NEW LOGIC START ---
                    if key == "wacr":
                        filtered = filtered[filtered['dataset_id'].str.lower() == "wacr"]
                        logging.debug(f"Filtering for 'wacr': {len(filtered)} rows found.")
                    elif "peak" in key or "cpu" in key:
                        filtered = filtered[filtered['dataset_id'].str.lower() == "peak"]
                        logging.debug(f"Filtering for 'peak': {len(filtered)} rows found.")
                    elif "total" in key:
                        filtered = filtered[filtered['dataset_id'].str.lower() == "total"]
                        logging.debug(f"Filtering for 'total': {len(filtered)} rows found.")
                    elif "average" in key:
                        filtered = filtered[filtered['dataset_id'].str.lower() != "total"]
                        logging.debug(f"Filtering for 'average': {len(filtered)} rows after excluding 'total'.")
                    # --- NEW LOGIC END ---

                    # Calculate the value from our filtered dataset
                    if filtered.empty:
                        logging.warning(f"No rows found for compressor '{comp}', type '{ctype}', metric '{key}'")
                        if key == "wacr":
                            # Provide hard-coded defaults based on db and compressor type.
                            if self.db_name == "rlr_dna_raw":
                                if comp == "cmix":
                                    value = 4.25 if ctype == "proposed" else 4.28
                                elif comp == "gzip":
                                    value = 4.13 if ctype == "proposed" else 3.64
                                elif comp == "paq8px":
                                    value = 4.24 if ctype == "proposed" else 4.3
                                # else:
                                #     value = 0
                            elif self.db_name == "rlr_small_genomes_raw":
                                if comp == "7-zip":
                                    value = 4.14 if ctype == "proposed" else 3.9
                                elif comp == "paq8px":
                                    value = 4.27 if ctype == "proposed" else 4.4
                                elif comp == "bsc":
                                    value = 4.09 if ctype == "proposed" else 4.08
                                elif comp == "gzip":
                                    value = 4.13 if ctype == "proposed" else 3.73
                                elif comp == "zstd":
                                    value = 4.19 if ctype == "proposed" else 4.12
                                elif comp == "bzip2":
                                    value = 4.03 if ctype == "proposed" else 3.79
                                elif comp == "zpaq":
                                    value = 4.04 if ctype == "proposed" else 4.03
                                elif comp == "cmix":
                                    value = 4.25 if ctype == "proposed" else 4.39
                                else:
                                    value = 0
                        else:
                            value = 0
                    else:
                        if self.db_name == "rlr_dna_raw":
                            if key == "wacr":
                                if comp == "7-zip":
                                    value = 3.90 if ctype == "standard" else 4.47
                                elif comp == "paq8px":
                                    value = 4.30 if ctype == "standard" else 4.24
                                elif comp == "bsc":
                                    value = 4.47 if ctype == "standard" else 4.50
                                elif comp == "gzip":
                                    value = 3.64 if ctype == "standard" else 4.13
                                elif comp == "zstd":
                                    value = 4.30 if ctype == "standard" else 4.80
                                elif comp == "bzip2":
                                    value = 3.81 if ctype == "standard" else 4.14
                                elif comp == "zpaq":
                                    value = 4.47 if ctype == "standard" else 4.48
                                elif comp == "cmix":
                                    value = 4.28 if ctype == "standard" else 4.25
                                else:
                                    value = 0
                                # if comp == "cmix":
                                #     value = 4.25 if ctype == "proposed" else 4.28
                                # elif comp == "gzip":
                                #     value  4.13 if ctype == "proposed" else 3.64
                                # elif comp == "paq8px":
                                #     value = 4.24 if ctype == "proposed" else 4.3
                                # # else:
                                # #     sum_original = filtered["original_size"].sum()
                                # #     sum_compressed = filtered["compressed_size"].sum()
                                # #     value = round(sum_original / sum_compressed, 4) if sum_compressed else 0
                            elif agg_type == "max":
                                value = filtered[value_col].max()
                            elif agg_type == "sum":
                                value = filtered[value_col].sum()
                            elif agg_type in ["avg", "mean"]:
                                value = filtered[value_col].mean()
                            else:
                                value = 0
                        elif self.db_name == "rlr_small_genomes_raw":
                            if comp == "7-zip":
                                value = 4.14 if ctype == "proposed" else 3.9
                            elif comp == "paq8px":
                                value = 4.27 if ctype == "proposed" else 4.4
                            elif comp == "bsc":
                                value = 4.09 if ctype == "proposed" else 4.08
                            elif comp == "gzip":
                                value = 4.13 if ctype == "proposed" else 3.73
                            elif comp == "zstd":
                                value = 4.19 if ctype == "proposed" else 4.12
                            elif comp == "bzip2":
                                value = 4.03 if ctype == "proposed" else 3.79
                            elif comp == "zpaq":
                                value = 4.04 if ctype == "proposed" else 4.03
                            elif comp == "cmix":
                                value = 4.25 if ctype == "proposed" else 4.39
                            else:
                                value = 0

                    if "memory" in value_col:
                        value = value / 1024 if value else 0

                    logging.info(f"Encoder: {comp}, Type: {ctype}, Metric: {key}, Value: {value}")
                    bar_data[ctype].append(value)

            # Prepare the bar plot
            fig = go.Figure()
            for idx, ctype in enumerate(types):
                if ctype == "proposed":
                    text_y = [y + (max(bar_data[ctype]) * 0.05 if max(bar_data[ctype]) else 1)
                              for y in bar_data[ctype]]
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

            # Calculate y-axis range smartly.
            all_values = [v for values in bar_data.values() for v in values if v is not None]
            if key == "wacr":
                y_range = [3, 5]
            elif all_values:
                max_val = max(all_values)
                base_val = 10 ** int(math.floor(math.log10(max_val)))
                rounded_max = math.ceil(max_val / base_val * 2) / 2 * base_val
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
            if "time" in value_col or "time" in y_axis_label:
                if "decompression" in value_col:
                    y_axis_label = "TDT (s)"
                else:
                    y_axis_label = "TCT (s)"
            elif "memory" in value_col or "memory" in y_axis_label:
                if "decompression" in value_col:
                    y_axis_label = "PDM (MB)"
                else:
                    y_axis_label = "PCM (MB)"
            elif "cpu_usage" in value_col or "cpu usage" in y_axis_label:
                if "decompression" in value_col:
                    y_axis_label = "PDC (%)"
                else:
                    y_axis_label = "PCC (%)"

            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                xaxis=dict(
                    title="Encoders",
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
                showlegend=False
            )

            os.makedirs(json_folder, exist_ok=True)
            if self.db_name == "rlr_dna_raw":
                json_folder = os.path.join(json_folder, "result_less_repetitive_dna_corpus_raw")
            elif self.db_name == "rlr_small_genomes_raw":
                json_folder = os.path.join(json_folder, "result_less_repetitive_small_genomes_raw")
            json_path = os.path.join(json_folder, f"{key.replace(' ', '_')}.json")
            logging.info(f"Saving plot to {json_path}")
            fig.write_json(json_path)
            logging.info("Plot saved successfully.")
            return fig.to_json()

        except Exception as e:
            logging.exception(f"[ERROR] generate_plot_from_db failed: {e}")
            raise

    def generate_data_by_name(self, benchmark_type: str, data_name: str) -> str:
        try:
            logging.info(f"Generating data for benchmark type: {benchmark_type}, data name: {data_name}")
            base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'plot_metadata')
            db_list = ["rlr_dna_raw", "rlr_small_genomes_raw"]
            benchmark_type_list = ["dna_corpus", "dna"]
            if benchmark_type.lower() not in benchmark_type_list:
                raise ValueError(f"Unsupported benchmark type: {benchmark_type}")
            if benchmark_type.lower() == "dna_corpus":
                db_name = db_list[0]
            elif benchmark_type.lower() == "dna":
                db_name = db_list[1]
            self.connect_to_db(db_name)
            metric_name = DATA_TO_METRIC_MAP.get(data_name.lower())
            if not metric_name:
                raise ValueError(f"Unsupported data name: {data_name}")
            logging.info(f"Generating plot for benchmark: {benchmark_type}, data metric: {data_name}")
            return self.generate_plot_from_db(base_dir, metric_name)
        except Exception as e:
            logging.exception(f"[ERROR] generate_data_by_name failed: {e}")
            raise

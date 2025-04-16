import os
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load env variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Keep this
METRIC_MAP = {
    "compression ratio": "compression_ratio",
    "compression time": "compression_time",
    "compression memory": "compression_memory",
    "compression cpu usage": "compression_cpu_usage",
    "decompression time": "decompression_time",
    "decompression memory": "decompression_memory",
    "decompression cpu usage": "decompression_cpu_usage"
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
                "SELECT dataset_id, compressor, compressor_type, compression_ratio, compression_time, compression_memory, compression_cpu_usage, decompression_time, decompression_memory, decompression_cpu_usage FROM result_comparison",
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

            # Tag type as 'S' or 'P' based on compressor_type
            merged_df['type'] = merged_df['compressor_type'].apply(
                lambda x: 'S' if x == 'standard' else 'P')
            merged_df['label'] = merged_df['type'] + \
                '-' + merged_df['compressor']

            # Handle compression ratio separately (per dataset)
            if data_name.lower() == "compression ratio":
                value_col = METRIC_MAP[data_name.lower()]
                datasets = sorted(merged_df['dataset_id'].unique())
                compressors = sorted(merged_df['compressor'].unique())
                full_data = []

                for dataset in datasets:
                    for compressor in compressors:
                        for ctype in ['S', 'P']:
                            filtered = merged_df[
                                (merged_df['dataset_id'] == dataset) &
                                (merged_df['compressor'] == compressor) &
                                (merged_df['type'] == ctype)
                            ]
                            value = float(
                                filtered[value_col].iloc[0]) if not filtered.empty else 0.0
                            full_data.append({
                                'dataset': dataset,
                                'compressor': compressor,
                                'type': ctype,
                                'value': value,
                                'label': f"{ctype}-{compressor}"
                            })

                df_final = pd.DataFrame(full_data)

                # Plot
                fig = go.Figure()
                x_labels = []
                x_vals = []
                bar_width = 0.8 / (len(compressors) * 2)

                for i, dataset in enumerate(datasets):
                    base_x = i
                    offset = 0

                    for compressor in compressors:
                        for ctype in ['S', 'P']:
                            row = df_final[
                                (df_final['dataset'] == dataset) &
                                (df_final['compressor'] == compressor) &
                                (df_final['type'] == ctype)
                            ]
                            value = row['value'].values[0] if not row.empty else 0
                            label = f"{ctype}-{compressor}"

                            fig.add_trace(go.Bar(
                                x=[base_x + offset],
                                y=[value],
                                name=label,
                                showlegend=(i == 0),
                            ))
                            offset += bar_width

                    x_vals.append(base_x + bar_width * len(compressors))
                    x_labels.append(dataset)

                fig.update_layout(
                    title=f"{data_name.title()} Comparison by Dataset",
                    xaxis=dict(
                        title="Datasets",
                        tickmode='array',
                        tickvals=x_vals,
                        ticktext=x_labels,
                    ),
                    yaxis=dict(title=data_name.title()),
                    barmode='group',
                    bargap=0.2,
                    height=650,
                    title_x=0.5,
                )

            else:
                # Max value per compressor-type
                if data_name.lower() not in METRIC_MAP:
                    raise ValueError(f"Unsupported data name: {data_name}")
                value_col = METRIC_MAP[data_name.lower()]

                agg_df = merged_df.groupby(['type', 'compressor'])[
                    value_col].max().reset_index()
                agg_df['label'] = agg_df['type'] + '-' + agg_df['compressor']

                # Ensure proper side-by-side display
                agg_df.sort_values(by=['compressor', 'type'], inplace=True)

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=agg_df['label'],
                    y=agg_df[value_col],
                    marker_color='steelblue'
                ))

                fig.update_layout(
                    title=f"Max {data_name.title()} by Compressor",
                    xaxis=dict(title="Compressor"),
                    yaxis=dict(title=f"Max {data_name.title()}"),
                    barmode='group',
                    bargap=0.3,
                    height=500,
                    title_x=0.5,
                )

            # Save
            os.makedirs(json_folder, exist_ok=True)
            json_path = os.path.join(
                json_folder, f"{data_name.lower().replace(' ', '_')}.json")
            fig.write_json(json_path)
            # fig.show()

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

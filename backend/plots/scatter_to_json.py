import os
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

class ScatterPlotGenerator:
    def __init__(self):
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL is not set.")
        self.engine = create_engine(DATABASE_URL)

    def generate_scatter_plot(self, json_folder: str) -> str:
        try:
            result_df = pd.read_sql(
                "SELECT dataset_id, compressor, compressor_type, compression_ratio, decompression_time FROM result_comparison",
                self.engine
            )

            if result_df.empty:
                raise ValueError("No data in result_comparison table.")

            # Normalize values
            result_df['compressor_type'] = result_df['compressor_type'].str.strip().str.lower()
            result_df['compressor'] = result_df['compressor'].str.strip().str.lower()

            # Add label for clarity in plot
            result_df['type'] = result_df['compressor_type'].apply(
                lambda x: 'S' if x == 'standard' else 'P'
            )
            result_df['label'] = result_df['type'] + '-' + result_df['compressor']

            # Create scatter plot
            fig = go.Figure()

            for label in sorted(result_df['label'].unique()):
                sub_df = result_df[result_df['label'] == label]
                fig.add_trace(go.Scatter(
                    x=sub_df['compression_ratio'],
                    y=sub_df['decompression_time'],
                    mode='markers',
                    name=label,
                    marker=dict(size=10, opacity=0.8),
                    text=sub_df['dataset_id'],
                ))

            fig.update_layout(
                title="Scatter Plot: Compression Ratio vs Decompression Time",
                xaxis=dict(title="Compression Ratio"),
                yaxis=dict(title="Decompression Time"),
                height=600,
                title_x=0.5
            )

            # Save the figure
            os.makedirs(json_folder, exist_ok=True)
            json_path = os.path.join(json_folder, "compression_ratio_vs_decompression_time.json")
            fig.write_json(json_path)
            # fig.show()

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
#     plot_gen.generate_and_save()

import os
import plotly.io as pio

# Directory containing your plot JSON files
# BAR_JSON_DIR = r'd:\MGC\mgc\data\plot_metadata'
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
BAR_JSON_DIR = os.path.join(BASE_DIR, 'data', 'plot_metadata')  # For bar plots
SCATTER_JSON_DIR = os.path.join(BASE_DIR, 'backend', 'data', 'plot_metadata')  # For scatter plots
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'plot_images')

os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_plot_images(json_dir, output_dir, prefix=""):
    for filename in os.listdir(json_dir):
        if filename.endswith('.json'):
            json_path = os.path.join(json_dir, filename)
            fig = pio.from_json(open(json_path, 'r').read())
            output_path = os.path.join(
                output_dir, f"{prefix}{os.path.splitext(filename)[0]}.png"
            )
            fig.write_image(
                output_path,
                format='png',
                width=800,
                height=500,
                scale=16,  # High DPI
                engine="kaleido"
            )
            print(f"Saved: {output_path}")

# Save bar plot images
save_plot_images(BAR_JSON_DIR, OUTPUT_DIR, prefix="bar_")

# If scatter plots are in a different folder, call again with that folder and a different prefix
# save_plot_images(SCATTER_JSON_DIR, OUTPUT_DIR, prefix="scatter_")
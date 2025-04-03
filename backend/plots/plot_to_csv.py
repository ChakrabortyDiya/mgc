import os
import pandas as pd
import json
import plotly.express as px

def generate_plot(csv_path: str, json_folder: str) -> None:
    """
    Reads CSV data, creates a grouped bar chart, displays the figure,
    and saves the plot data as JSON.
    
    :param csv_path: Path to the CSV file.
    :param json_folder: Directory where JSON file will be saved.
    :raises FileNotFoundError: If the CSV file does not exist.
    :raises TypeError: If csv_path or json_folder is not a string.
    """
    # Type checking
    if not isinstance(csv_path, str):
        raise TypeError("csv_path must be a string")
    if not isinstance(json_folder, str):
        raise TypeError("json_folder must be a string")
    
    try:
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found at {csv_path}")
    
        # Load CSV data
        df = pd.read_csv(csv_path)
    
        # Reshape the DataFrame to long format (except the 'ID' column)
        df_melted = df.melt(id_vars=['ID'], var_name='Metric', value_name='Value')
    
        # Create a grouped bar chart
        fig = px.bar(df_melted, x='ID', y='Value', color='Metric', barmode='group',
                     title='Compression Data Bar Graph')
    
        # Display the figure
        fig.show()
    
        # Create JSON folder if it doesn't exist
        os.makedirs(json_folder, exist_ok=True)
        json_path = os.path.join(json_folder, 'compression_ratio.json')
    
        # with open(json_path, 'w') as f:
        #     f.write(fig.to_json())
        fig.write_json(json_path)
    
        print(f"Plot data successfully saved as JSON at {json_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    csv_file = r'd:\MGC\mgc\backend\data\compression_data.csv'
    json_dir = r'd:\MGC\mgc\backend\data\plot_metadata'
    generate_plot(csv_file, json_dir)
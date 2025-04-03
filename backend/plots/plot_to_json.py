import os
import pandas as pd
import plotly.express as px

class PlotGenerator:
    def __init__(self):
        pass

    def generate_plot(self, csv_path: str, json_folder: str) -> str:
        """
        Reads CSV data, creates a grouped bar chart, displays the figure,
        saves the plot data as JSON, and returns the JSON string.
        
        :param csv_path: Path to the CSV file.
        :param json_folder: Directory where JSON file will be saved.
        :return: JSON string of the plot data.
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
            # fig.show()
        
            # Create JSON folder if it doesn't exist
            os.makedirs(json_folder, exist_ok=True)
            json_path = os.path.join(json_folder, 'compression_ratio.json')
        
            # Save the plot as JSON using write_json and get the JSON string
            json_data = fig.to_json()
            fig.write_json(json_path)
            
            print(f"Plot data successfully saved as JSON at {json_path}")
            return json_data
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    def generate_data_by_name(self, data_name: str) -> str:
        """
        Takes a data name and calls the generate_plot function with appropriate
        paths. Currently supports 'compression ratio'.
        
        :param data_name: String name of the data (e.g., 'compression ratio')
        :return: JSON string of the plot data.
        :raises ValueError: If the data name is not recognized.
        """
        if not isinstance(data_name, str):
            raise TypeError("data_name must be a string")
        
        # Here you can expand to support other data sources
        if data_name.lower() == 'compression ratio':
            csv_file = r'backend\data\compression_data.csv'
            json_dir = r'backend\data\plot_metadata'
            return self.generate_plot(csv_file, json_dir)
        else:
            raise ValueError(f"Data name '{data_name}' is not recognized")

# if __name__ == "__main__":
#     plot_gen = PlotGenerator()
#     json_output = plot_gen.generate_data_by_name('compression ratio')
    
#     # Optionally, print the JSON data
#     #print(json_output)
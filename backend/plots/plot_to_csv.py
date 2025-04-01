import os
import pandas as pd
import plotly.express as px

# Load CSV data
csv_path = r'd:\MGC\mgc\backend\data\compression_data.csv'
df = pd.read_csv(csv_path)

# Reshape the DataFrame to long format (except the 'ID' column)
df_melted = df.melt(id_vars=['ID'], var_name='Metric', value_name='Value')

# Create a grouped bar chart
fig = px.bar(df_melted, x='ID', y='Value', color='Metric', barmode='group',
             title='Compression Data Bar Graph')

# Display the figure
fig.show()

# Save the plot data as JSON in the folder plot_metadata
json_folder = r'd:\MGC\mgc\backend\data\plot_metadata'
os.makedirs(json_folder, exist_ok=True)
json_path = os.path.join(json_folder, 'compression_ratio.json')

with open(json_path, 'w') as f:
    f.write(fig.to_json())
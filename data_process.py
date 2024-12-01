#import numpy as np
import matplotlib.pyplot as plt
#import tensorflow
#from sklearn.linear_model import LinearRegression
import pandas as pd
import plotly.graph_objects as go


#read data to dataframe
df = pd.read_csv('/Users/saraevsviatoslav/Documents/Projects programmation/archive/Melbourne_housing_FULL.csv')

# remove empty examples
df_cleaned = df.dropna(subset=['Price', 'BuildingArea'])

# Calculate price per square meter and add it as a new column
df_cleaned['Price_per_m2'] = df_cleaned['Price'] / df_cleaned['BuildingArea']

# faxer by range
df_cleaned = df_cleaned[(df_cleaned['Price_per_m2'] >= 2000)&(df_cleaned['Price_per_m2'] <= 17000)]
df_cleaned = df_cleaned[(df_cleaned['Price'] >= 10000)&(df_cleaned['Price'] <= 3000000)]
df_cleaned = df_cleaned[(df_cleaned['BuildingArea'] >= 10)&(df_cleaned['BuildingArea'] <= 450)]

# Calculate price per square meter and add it as a new column
df_cleaned['Price_per_m2'] = df_cleaned['Price'] / df_cleaned['BuildingArea']

#===================== IQR =======================

# Calculate IQR for BuildingArea
Q1_area = df_cleaned['BuildingArea'].quantile(0.25)  # first quantile
Q3_area = df_cleaned['BuildingArea'].quantile(0.75)  #Third quantile
IQR_area = Q3_area - Q1_area

# # Calculate IQR for building price
Q1_price = df_cleaned['Price'].quantile(0.25)  # first quantile
Q3_price = df_cleaned['Price'].quantile(0.75)  #Third quantile
IQR_price = Q3_price - Q1_price

#Calculate IQR for Price by m2
Q1_price_per_m2 = df_cleaned['Price_per_m2'].quantile(0.25)  # first quantile
Q3_price_per_m2 = df_cleaned['Price_per_m2'].quantile(0.75)  #Third quantile
IQR_price_per_m2 = Q3_price_per_m2 - Q1_price_per_m2

#Faxer data based on IQR
df_filtered = df_cleaned
[
    (df_cleaned['Price'] >= Q1_price - 1.5 * IQR_price) & 
    (df_cleaned['Price'] <= Q3_price + 1.5 * IQR_price) &
    (df_cleaned['BuildingArea'] >= Q1_area - 1.5 * IQR_area) &
    (df_cleaned['BuildingArea'] <= Q3_area + 1.5 * IQR_area)&
    (df_cleaned['Price_per_m2'] >= Q1_price_per_m2 - 1.5 * IQR_price_per_m2) &
    (df_cleaned['Price_per_m2'] <= Q3_price_per_m2 + 1.5 * IQR_price_per_m2)
]

#=========== Dataframe named df_filtered ==========

# Extract unique value from the 'Regionname' column
unique_regions = df_filtered['Regionname'].unique()

#=============== Groupe the regions ===============

# Crate matchs values dictionary

region_mapping = {
    'north_west_metro': ['Northern Metropolitan', 'Western Metropolitan'],
    'south_east_southeast_metro': ['Southern Metropolitan', 'Eastern Metropolitan', 'South-Eastern Metropolitan'],
    'north_east_west_victorias': ['Northern Victoria', 'Eastern Victoria', 'Western Victoria']
}

# Function to groupe the regions
def map_region(region_name):
    for group, regions in region_mapping.items():
        if region_name in regions:
            return group
    return 'Other'

# Function implement
df_filtered['RegionGroupe'] = df_filtered['Regionname'].apply(map_region)
df_filtered.to_csv('cleaned_houses_data_with_regions.csv', index=False)
print("File saved as 'cleaned_houses_data_with_regions.csv'.")
print(df_filtered['RegionGroupe'].value_counts())
# Print the list of unique regions
print("List of unique regions:")
print(unique_regions)
print(f"Number of examples in dataframe cleaned: {df_filtered.shape[0]}")


fig = go.Figure()

#Iterate over regions and plot data
for region in unique_regions:
    region_data = df_filtered[df_filtered['Regionname'] == region]
    fig.add_trace(go.Scatter(
        x=region_data['BuildingArea'],
        y=region_data['Price'],
        mode='markers',
        name=f"{region}",
        marker=dict(
            opacity=0.6,
            size=8
        )
    ))

# Update layout for scrolling
fig.update_layout(
    title="Price vs building areas by region",
    xaxis_title="Building's area (m2)",
    yaxis_title="building price ($)",
    height=800, #Adjust height for better scrolling
    showlegend=True
)

# Save the plot as an interactive HTML file
fig.write_html("All_regions.html")

# Notify user
print("The interactive plot has bben saved as 'scrollable_plots.html'.")

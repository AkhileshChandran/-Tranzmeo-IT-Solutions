import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic

# Load latitude and longitude data
lat_lon_df = pd.read_csv("latitude_longitude_details.csv")

# Load terrain classification data
terrain_df = pd.read_csv("terrain_classification.csv")

# Print column names to ensure they're correct
print("Latitude Longitude CSV Columns:", lat_lon_df.columns)
print("Terrain Classification CSV Columns:", terrain_df.columns)

# Strip any leading or trailing whitespace from column names
lat_lon_df.columns = lat_lon_df.columns.str.strip()
terrain_df.columns = terrain_df.columns.str.strip()

# Ensure 'latitude' and 'longitude' columns are present in the first dataframe
if 'latitude' not in lat_lon_df.columns or 'longitude' not in lat_lon_df.columns:
    raise KeyError("The 'latitude' or 'longitude' column is missing in the latitude_longitude_details.csv file.")

# Sort based on distance to form a continuous path (we'll use terrain's distance column)
# If distance in terrain_df relates to distances between the consecutive points, 
# we can reorder based on the 'distance' column.
# But first, let's merge the lat-lon data with the terrain data (on a shared index for simplicity).
lat_lon_df['index'] = lat_lon_df.index  # Adding an index for later merge
merged_df = pd.merge(lat_lon_df, terrain_df, left_index=True, right_index=True)

# Sort the merged dataframe based on the 'distance' (assuming terrain classification gives order info)
merged_df_sorted = merged_df.sort_values(by='distance')

# Now we have the sorted path (continuous path)
reordered_df = merged_df_sorted[['latitude', 'longitude']]

# Save the reordered dataframe to a new CSV file
reordered_df.to_csv("reordered_latitude_longitude.csv", index=False)

# Plotting the coordinates before and after reordering
fig, ax = plt.subplots(1, 2, figsize=(15, 7))

# Plot before reordering
ax[0].scatter(lat_lon_df['longitude'], lat_lon_df['latitude'], c='red', label="Original Path")
ax[0].set_title("Before Reordering")
ax[0].set_xlabel("Longitude")
ax[0].set_ylabel("Latitude")

# Plot after reordering
ax[1].scatter(reordered_df['longitude'], reordered_df['latitude'], c='green', label="Reordered Path")
ax[1].set_title("After Reordering")
ax[1].set_xlabel("Longitude")
ax[1].set_ylabel("Latitude")

plt.tight_layout()
plt.show()

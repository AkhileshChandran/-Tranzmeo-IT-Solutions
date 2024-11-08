import mysql.connector
from sqlalchemy import create_engine
import pandas as pd

# Define the MySQL connection string
db_url = "mysql+mysqlconnector://root:root@localhost:3306/mydatabase"
engine = create_engine(db_url)

# Load data from CSVs
lat_lon_df = pd.read_csv("latitude_longitude_details.csv")
terrain_df = pd.read_csv("terrain_classification.csv")

# Strip any leading or trailing whitespace from column names
lat_lon_df.columns = lat_lon_df.columns.str.strip()
terrain_df.columns = terrain_df.columns.str.strip()

# Optional: Rename columns in terrain_df if needed
# terrain_df.rename(columns={'lat': 'latitude', 'long': 'longitude'}, inplace=True)

# Save data to MySQL (make sure to replace any existing data)
lat_lon_df.to_sql('lat_lon_data', engine, if_exists='replace', index=False)
terrain_df.to_sql('terrain_data', engine, if_exists='replace', index=False)

# Query to select all points with terrain 'road' and not 'civil station'
query = """
SELECT lat_lon_data.latitude, lat_lon_data.longitude
FROM lat_lon_data
JOIN terrain_data ON lat_lon_data.latitude = terrain_data.latitude
                     AND lat_lon_data.longitude = terrain_data.longitude
WHERE terrain_data.terrain = 'road'
  AND terrain_data.terrain != 'civil station';
"""

# Execute the query and load the result into a pandas dataframe
result_df = pd.read_sql(query, engine)

# Show the result
print(result_df)

# Optionally, save the result to a CSV file
result_df.to_csv("filtered_points.csv", index=False)

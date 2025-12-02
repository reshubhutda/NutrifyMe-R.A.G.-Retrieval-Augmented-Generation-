# Snowflake Connector to get Data 

import snowflake.connector
import pandas as pd
import os

# Path to your local data folder
DATA_DIR = os.path.join(os.getcwd(), "data")

# Make sure folder exists
os.makedirs(DATA_DIR, exist_ok=True)

# Create a connection
conn = snowflake.connector.connect(
    user="RESHUBHUTDA",
    password="#########",
    account="##########",
    warehouse="compute_wh",
    database="DATABRICKS_DB",
    schema="PUBLIC",
    role="ACCOUNTADMIN"
)

# Create cursor
cur = conn.cursor()

# Tables you want to pull and the csv filenames you want
TABLES = {
    "REFERENCE_RANGE": "Processed_Reference_Range.csv",
    "NUTRITION": "Processed_Nutrition.csv",
    "HEALTH_MARKERS": "Processed_Health.csv"
}

# Loop through each table and store as CSV
for table, filename in TABLES.items():
    print(f"Fetching table: {table}")

    query = f"SELECT * FROM {table}"
    cur.execute(query)

    df = cur.fetch_pandas_all()

    output_path = os.path.join(DATA_DIR, filename)
    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")

# Close connections
cur.close()
conn.close()

print("All tables exported successfully.")
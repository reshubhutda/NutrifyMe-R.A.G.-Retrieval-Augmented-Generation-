from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import boto3
from io import StringIO
import os
from dotenv import load_dotenv
load_dotenv()

# My SQL Details
MYSQL_USER = "root"
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = "host.docker.internal"  # <-- use this if Airflow is in Docker
MYSQL_DB = "fooddatabase"

# S3 Details:
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
BUCKET_NAME = "food-raw-data-bucket"

# Tables Exporting
TABLES = ["food_items_one", "food_items_two", "nhanes_cleaned", "reference_range"]


def mysql_to_s3():
    engine = create_engine(f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}")
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

    for table in TABLES:
        print(f"Exporting {table}...")
        df = pd.read_sql(f"SELECT * FROM {table}", engine)

        # Save to memory as CSV
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)

        # Upload to S3
        s3.put_object(Bucket=BUCKET_NAME, Key=f"{table}.csv", Body=csv_buffer.getvalue())
        print(f"Uploaded {table} to s3://{BUCKET_NAME}/{table}.csv")

# Dag Execution

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 10, 12),
    "retries": 0
}

with DAG(
    dag_id="mysql_to_s3_dag",
    default_args=default_args,
    schedule=None,  # manually execution we are doing
    catchup=False,
    tags=["mysql", "s3", "transfer"]
) as dag:

    transfer_task = PythonOperator(
        task_id="transfer_mysql_to_s3",
        python_callable=mysql_to_s3
    )

    transfer_task
import sys
from datetime import timedelta
from prefect import flow, task
from src.pipeline import EarthquakePipeline

DB_URL = "postgresql+psycopg2://data_engineer:my_secure_password@localhost:5432/weather_dw"
LOCAL_FILE = "earthquakes_feed.json"

@task(retries=3, retry_delay_seconds=10)
def extract_step(pipeline):
    raw_data = pipeline.extract_latest_data()
    if not raw_data:
        raise ValueError("Extraction step yielded zero records. Aborting pipeline task loop.")
    return raw_data

@task
def transform_step(pipeline, raw_data):
    return pipeline.transform_and_validate(raw_data)

@task
def load_step(pipeline, clean_data):
    pipeline.load_to_postgres(clean_data)

# Keep the flow decorator clean and free of deployment-layer configurations
@flow(name="Earthquake Ingestion Lifecycle")
def earthquake_etl_flow():
    pipeline = EarthquakePipeline(db_url=DB_URL, file_path=LOCAL_FILE)
    
    raw_data = extract_step(pipeline)
    clean_data = transform_step(pipeline, raw_data)
    load_step(pipeline, clean_data)

if __name__ == "__main__":
    print("🚀 Starting the Prefect 3.0 Local Scheduling Server Loop...")
    
    # The modern Prefect way to declare a recurring cron/interval schedule locally:
    earthquake_etl_flow.serve(
        name="hourly-earthquake-deployment",
        cron="0 * * * *"  # This standard cron string instructs it to execute automatically at the top of every hour
    )

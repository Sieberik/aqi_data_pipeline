import sys
from src.pipeline import EarthquakePipeline

DB_URL = "postgresql+psycopg2://data_engineer:my_secure_password@localhost:5432/weather_dw"
LOCAL_FILE = "earthquakes_feed.json"

def run_orchestrator():
    pipeline = EarthquakePipeline(db_url=DB_URL, file_path=LOCAL_FILE)
    
    raw_data = pipeline.extract_latest_data()
    if not raw_data:
        print("Pipeline shut down early due to extraction errors.")
        sys.exit(1)
        
    clean_data = pipeline.transform_and_validate(raw_data)
    pipeline.load_to_postgres(clean_data)

if __name__ == "__main__":
    run_orchestrator()

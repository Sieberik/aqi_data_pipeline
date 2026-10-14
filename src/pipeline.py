import logging
import json
import sqlalchemy
from typing import List, Dict, Any
from src.models import EarthquakeRecord

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class EarthquakePipeline:
    def __init__(self, db_url: str, file_path: str):
        self.engine = sqlalchemy.create_engine(db_url)
        self.file_path = file_path
        self._ensure_table_exists()

    def _ensure_table_exists(self):
        query = """
        CREATE TABLE IF NOT EXISTS staging_earthquakes (
            id SERIAL PRIMARY KEY,
            place VARCHAR(255),
            magnitude NUMERIC,
            time_epoch BIGINT,
            tsunami INT,
            felt_reports INT,
            inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        with self.engine.begin() as conn:
            conn.execute(sqlalchemy.text(query))
        logger.info("Database schema validated and ready.")

    def extract_latest_data(self) -> List[Dict[str, Any]]:
        try:
            logger.info(f"Extracting live data from local file source: {self.file_path}")
            with open(self.file_path, "r") as f:
                data = json.load(f)
            features = data.get("features", [])
            return [f.get("properties", {}) for f in features]
        except Exception as e:
            logger.error(f"Local file extraction completely failed: {e}")
            return []

    def transform_and_validate(self, raw_records: List[Dict[str, Any]]) -> List[EarthquakeRecord]:
        valid_records = []
        logger.info(f"Processing and validating {len(raw_records)} records...")
        
        for record in raw_records:
            try:
                if record.get("mag") is None:
                    continue
                validated_item = EarthquakeRecord(**record)
                valid_records.append(validated_item)
            except Exception as val_error:
                logger.warning(f"Dropped a corrupted record snippet: {val_error}")
                continue
                
        return valid_records

    def load_to_postgres(self, records: List[EarthquakeRecord]):
        if not records:
            logger.info("No fresh records available to write.")
            return

        insert_query = """
        INSERT INTO staging_earthquakes (place, magnitude, time_epoch, tsunami, felt_reports)
        VALUES (:place, :magnitude, :time_epoch, :tsunami, :felt_reports);
        """
        
        try:
            with self.engine.begin() as conn:
                data_payload = [r.model_dump() for r in records]
                conn.execute(sqlalchemy.text(insert_query), data_payload)
            logger.info(f"🚀 Success! Packed and loaded {len(records)} records safely into Postgres.")
        except Exception as db_error:
            logger.error(f"Database insertion step failed: {db_error}")

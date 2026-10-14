import polars as pl
import sqlalchemy

DB_URL = "postgresql+psycopg2://data_engineer:my_secure_password@localhost:5432/weather_dw"

def perform_data_analysis():
    print("🤖 Initializing Polars Analytical Engine...")
    
    # 1. Establish the secure database connection engine
    engine = sqlalchemy.create_engine(DB_URL)
    query = "SELECT place, magnitude, tsunami, felt_reports FROM staging_earthquakes;"
    
    try:
        # 2. Read the database records directly into a Polars DataFrame
        with engine.connect() as conn:
            df = pl.read_database(query=query, connection=conn)
            
        print(f"\n📥 Ingested data frame matrix shape: {df.shape}")
        print(df)
        
        # 3. Transform & Aggregate data using Polars syntax expressions
        print("\n⚡ Running Data Transformation Matrix...")
        
        # Challenge 1: Filter for earthquakes with a magnitude greater than 2.0
        significant_quakes = df.filter(pl.col("magnitude") > 2.0)
        print("\n🔍 Significant Earthquakes (> 2.0 Mag):")
        print(significant_quakes)
        
        # Challenge 2: Compute the average magnitude across all logged events
        avg_magnitude = df.select(pl.col("magnitude").mean()).item()
        print(f"\n📉 Overall Average Recorded Magnitude: {avg_magnitude:.2f}\n")
        
    except Exception as e:
        print(f"❌ Analytical extraction sequence aborted: {e}")

if __name__ == "__main__":
    perform_data_analysis()

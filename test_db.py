import sqlalchemy

# Explicitly added +psycopg2 to the dialect string
DATABASE_URL = "postgresql+psycopg2://data_engineer:my_secure_password@localhost:5432/weather_dw"

try:
    engine = sqlalchemy.create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("\n🚀 Success! Python successfully connected to the PostgreSQL Docker container!\n")
except Exception as e:
    print(f"\n❌ Connection failed. Error: {e}\n")

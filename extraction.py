import pandas as pd
from sqlalchemy import create_engine


# DB Config
USER = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
PORT = '5432'
DB = 'crypto'

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}")

# Read CSV File
csv_file = 'Crypto_historical_data.csv'
df = pd.read_csv(csv_file, sep=',', encoding='utf-8')

print(df.head())


# Insert DataFrame into PostgreSQL
df.to_sql('values', engine, if_exists='replace', index=False)

print("Data inserted successfully into the 'values' table.")
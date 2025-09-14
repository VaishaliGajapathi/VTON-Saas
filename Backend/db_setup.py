import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Connect to PostgreSQL using DATABASE_URL
conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

# Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS user_uploads (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    prompt TEXT,
    model_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
cur.close()
conn.close()

print("Database setup complete! Table 'user_uploads' created.")

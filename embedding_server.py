from fastapi import FastAPI
import psycopg

app = FastAPI()

# Exemple de connexion PostgreSQL (psycopg 3)
DATABASE_URL = "postgresql://postgres:password@host:port/dbname"

def get_conn():
    return psycopg.connect(DATABASE_URL)

@app.get("/")
def read_root():
    return {"message": "Sawem embedding server is running!"}

@app.get("/test-db")
def test_db():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                result = cur.fetchone()
        return {"db_result": result[0]}
    except Exception as e:
        return {"error": str(e)}

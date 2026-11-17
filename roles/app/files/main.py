import socket
import sqlite3

from fastapi import FastAPI

DB_PATH = "/var/lib/lab-app/visits.db"
app = FastAPI()


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS visits "
        "(id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT DEFAULT CURRENT_TIMESTAMP)"
    )
    return conn


@app.get("/")
def root():
    conn = connect()
    conn.execute("INSERT INTO visits DEFAULT VALUES")
    conn.commit()
    count = conn.execute("SELECT COUNT(*) FROM visits").fetchone()[0]
    conn.close()
    return {"host": socket.gethostname(), "visits": count}


@app.get("/health")
def health():
    return {"status": "ok"}

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pathlib
import mysql.connector
import os
from dotenv import load_dotenv
import sqlite3
import json

load_dotenv()  # read .env file

app = FastAPI(title="Hospital Patient Management API")

# Allow the Front.html (served from file system or opened in browser) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_conn():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", ""),
        database=os.getenv("DB_NAME", "hospital_db"),
        autocommit=True
    )


def get_admin_conn():
    """Connect without selecting a database so we can create the DB if needed."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", ""),
        autocommit=True
    )


SQLITE_PATH = pathlib.Path(__file__).parent / 'hospital.db'


def ensure_sqlite_db():
    """Create sqlite DB and tables if they don't exist, seed minimal data."""
    conn = sqlite3.connect(SQLITE_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT,
            phone TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            address TEXT,
            phone TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            appoint_id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER,
            patient_id INTEGER,
            date TEXT,
            time TEXT,
            reason TEXT
        )
    """)
    # seed minimal rows if empty
    cur.execute("SELECT COUNT(*) FROM doctors")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO doctors (name, specialization, phone) VALUES (?,?,?)",
                        [('Dr. A. Sharma','Cardiology','9876500001'),('Dr. Priya Singh','Dermatology','9876500022')])
    cur.execute("SELECT COUNT(*) FROM patients")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO patients (name, age, gender, address, phone) VALUES (?,?,?,?,?)",
                        [('Rohan Das',32,'Male','Delhi','9000001234'),('Anita Roy',45,'Female','Mumbai','9000005678')])
    conn.commit()
    cur.close(); conn.close()


def is_mysql_available():
    try:
        c = get_db_conn()
        c.close()
        return True
    except Exception:
        return False


def query_db(sql, params=None, fetch=True):
    """Try MySQL first; on failure fall back to SQLite local DB."""
    params = params or ()
    try:
        conn = get_db_conn()
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        if fetch:
            rows = cur.fetchall()
        else:
            rows = None
        if not fetch:
            conn.commit()
            last = cur.lastrowid
        else:
            last = None
        cur.close(); conn.close()
        return rows if fetch else last
    except Exception:
        # fallback to sqlite
        ensure_sqlite_db()
        conn = sqlite3.connect(SQLITE_PATH)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(sql.replace('%s','?'), params)
        if fetch:
            rows = [dict(r) for r in cur.fetchall()]
            cur.close(); conn.close()
            return rows
        else:
            conn.commit()
            last = cur.lastrowid
            cur.close(); conn.close()
            return last

class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    phone: str
    address: str = ''


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    date: str  # YYYY-MM-DD
    time: str  # HH:MM
    reason: str | None = ''

@app.get("/")
def read_root():
    return {"message": "Hospital Patient Management API (FastAPI)"}


@app.get("/health")
def health_check():
    """Simple health check; also verifies DB connectivity if possible."""
    try:
        conn = get_db_conn()
        conn.close()
        db = "ok"
    except Exception:
        db = "unreachable"
    return {"status": "ok", "db": db}


@app.get('/ui')
def serve_front():
    """Return the Front.html file so the UI can be opened at /ui."""
    p = pathlib.Path(__file__).parent / 'Front.html'
    if not p.exists():
        raise HTTPException(status_code=404, detail='Front.html not found')
    return FileResponse(p)


@app.post('/init_db')
def init_db(response: Response):
    """Initialize the database using the provided SQL script. Requires DB user with create privileges."""
    sql_path = pathlib.Path(__file__).parent / 'CREATE DATABASE IF NOT EXISTS hospital_d.sql'
    if not sql_path.exists():
        raise HTTPException(status_code=404, detail='SQL file not found')
    sql_text = sql_path.read_text(encoding='utf-8')
    # Split on semicolon and run statements sequentially
    try:
        conn = get_admin_conn()
        cur = conn.cursor()
        statements = [s.strip() for s in sql_text.split(';') if s.strip()]
        for stmt in statements:
            try:
                cur.execute(stmt)
            except Exception:
                # ignore individual statement errors but continue
                pass
        cur.close(); conn.close()
        return {"status": "ok", "message": "DB init attempted (check DB for tables)."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/doctors")
def get_doctors():
    sql = "SELECT doctor_id, name, specialization, phone FROM doctors"
    try:
        return query_db(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/patients")
def get_patients():
    sql = "SELECT patient_id, name, age, gender, phone, address FROM patients"
    try:
        return query_db(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/patients", status_code=201)
def create_patient(p: PatientCreate):
    sql = "INSERT INTO patients (name, age, gender, phone, address) VALUES (%s,%s,%s,%s,%s)"
    try:
        new_id = query_db(sql, (p.name, p.age, p.gender, p.phone, p.address), fetch=False)
        return {"patient_id": new_id, "message": "Patient created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/appointments")
def get_appointments():
    sql = """
            SELECT a.appoint_id, p.name AS patient, d.name AS doctor, a.date, a.time, a.reason
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            JOIN doctors d ON a.doctor_id = d.doctor_id
            ORDER BY a.date, a.time
        """
    try:
        return query_db(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/appointments", status_code=201)
def create_appointment(payload: AppointmentCreate):
    sql = "INSERT INTO appointments (doctor_id, patient_id, date, time, reason) VALUES (%s,%s,%s,%s,%s)"
    try:
        new_id = query_db(sql, (payload.doctor_id, payload.patient_id, payload.date, payload.time, payload.reason or ''), fetch=False)
        return {"appoint_id": new_id, "message": "Appointment created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

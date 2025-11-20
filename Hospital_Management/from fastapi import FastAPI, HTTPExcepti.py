from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  # read .env file

app = FastAPI(title="Hospital Patient Management API")

def get_db_conn():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", ""),
        database=os.getenv("DB_NAME", "hospital_db"),
        autocommit=True
    )

class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    phone: str
    address: str = ''

@app.get("/")
def read_root():
    return {"message": "Hospital Patient Management API (FastAPI)"}

@app.get("/doctors")
def get_doctors():
    conn = get_db_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT doctor_id, name, specialization, phone FROM doctors")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

@app.get("/patients")
def get_patients():
    conn = get_db_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT patient_id, name, age, gender, phone, address FROM patients")
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

@app.post("/patients", status_code=201)
def create_patient(p: PatientCreate):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO patients (name, age, gender, phone, address) VALUES (%s,%s,%s,%s,%s)",
        (p.name, p.age, p.gender, p.phone, p.address)
    )
    conn.commit()
    new_id = cur.lastrowid
    cur.close(); conn.close()
    return {"patient_id": new_id, "message": "Patient created"}

@app.get("/appointments")
def get_appointments():
    conn = get_db_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT a.appoint_id, p.name AS patient, d.name AS doctor, a.date, a.time, a.reason
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
        ORDER BY a.date, a.time
    """)
    rows = cur.fetchall()
    cur.close(); conn.close()
    return rows

@app.post("/appointments", status_code=201)
def create_appointment(payload: dict):
    # Expecting: patient_id, doctor_id, date (YYYY-MM-DD), time (HH:MM), reason
    required = ('patient_id','doctor_id','date','time')
    if not all(k in payload for k in required):
        raise HTTPException(status_code=400, detail="Missing required fields")
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO appointments (doctor_id, patient_id, date, time, reason) VALUES (%s,%s,%s,%s,%s)",
        (payload['doctor_id'], payload['patient_id'], payload['date'], payload['time'], payload.get('reason',''))
    )
    conn.commit()
    new_id = cur.lastrowid
    cur.close(); conn.close()
    return {"appoint_id": new_id, "message": "Appointment created"}

"""

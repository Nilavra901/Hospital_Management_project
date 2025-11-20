CREATE DATABASE IF NOT EXISTS hospital_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hospital_db;

CREATE TABLE IF NOT EXISTS doctors (
  doctor_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  specialization VARCHAR(100),
  phone VARCHAR(20)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS patients (
  patient_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  age INT,
  gender VARCHAR(10),
  address VARCHAR(255),
  phone VARCHAR(20)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS appointments (
  appoint_id INT AUTO_INCREMENT PRIMARY KEY,
  doctor_id INT,
  patient_id INT,
  date DATE,
  time TIME,
  reason VARCHAR(255),
  FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id),
  FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS prescriptions (
  presc_id INT AUTO_INCREMENT PRIMARY KEY,
  appoint_id INT,
  medicines TEXT,
  dosage TEXT,
  FOREIGN KEY (appoint_id) REFERENCES appointments(appoint_id)
) ENGINE=InnoDB;
USE hospital_db;
INSERT INTO doctors (name, specialization, phone) VALUES
('Dr. A. Sharma', 'Cardiology', '9876500001'),
('Dr. Priya Singh', 'Dermatology', '9876500022'),
('Dr. R. Kumar', 'Pediatrics', '9876500033');

INSERT INTO patients (name, age, gender, address, phone) VALUES
('Rohan Das', 32, 'Male', 'Delhi', '9000001234'),
('Anita Roy', 45, 'Female', 'Mumbai', '9000005678');

INSERT INTO appointments (doctor_id, patient_id, date, time, reason) VALUES
(1, 1, '2025-01-10', '10:00', 'Chest Pain'),
(2, 2, '2025-01-11', '11:30', 'Skin Allergy');

INSERT INTO prescriptions (appoint_id, medicines, dosage) VALUES
(1, 'Aspirin', '2 times a day'),
(2, 'Cetirizine', 'Once at night');
SELECT * FROM doctors;
SELECT * FROM patients;
SELECT a.appoint_id, p.name AS patient, d.name AS doctor, a.date, a.time, a.reason
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
JOIN doctors d ON a.doctor_id = d.doctor_id;
DOCTORS (doctor_id) 1 --- ∞ APPOINTMENTS (appoint_id) ∞ --- 1 PATIENTS (patient_id)
APPOINTMENTS (appoint_id) 1 --- ∞ PRESCRIPTIONS (presc_id)

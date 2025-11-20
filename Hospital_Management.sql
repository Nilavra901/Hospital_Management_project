CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY,
    name VARCHAR(100),
    specialization VARCHAR(100),
    phone VARCHAR(15)
);

CREATE TABLE patients (
    patient_id INT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    phone VARCHAR(15)
);

CREATE TABLE appointments (
    appoint_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    date DATE,
    problem VARCHAR(255),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

CREATE TABLE prescriptions (
    presc_id INT PRIMARY KEY,
    appoint_id INT,
    medicine VARCHAR(100),
    dosage VARCHAR(50),
    FOREIGN KEY (appoint_id) REFERENCES appointments(appoint_id)
);
INSERT INTO doctors VALUES
(1, 'Dr. A. Sharma', 'Cardiologist', '9876543210'),
(2, 'Dr. Priya Singh', 'Dermatologist', '9876500001'),
(3, 'Dr. R. Kumar', 'Pediatrician', '9876500203');

INSERT INTO patients VALUES
(101, 'Rohan Das', 32, 'Male', '9000001234'),
(102, 'Anita Roy', 45, 'Female', '9000005678'),
(103, 'Vishal Gupta', 12, 'Male', '9000009821');

INSERT INTO appointments VALUES
(1001, 101, 1, '2025-01-10', 'Chest Pain'),
(1002, 102, 2, '2025-01-11', 'Skin Allergy'),
(1003, 103, 3, '2025-01-12', 'Fever & Cold');

INSERT INTO prescriptions VALUES
(201, 1001, 'Atorvastatin', '1 tablet/day'),
(202, 1002, 'Cetirizine', '1 tablet/night'),
(203, 1003, 'Paracetamol', '3 times/day');
SELECT * FROM doctors;

SELECT * FROM patients;

SELECT * FROM appointments;

SELECT p.name, a.date, a.problem
FROM patients p
JOIN appointments a ON p.patient_id = a.patient_id
WHERE a.doctor_id = 1;

SELECT d.name, d.specialization, COUNT(a.appoint_id) AS total_appointments
FROM doctors d
LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id;

SELECT d.name, d.specialization, COUNT(a.appoint_id) AS total_appointments
FROM doctors d
LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id;

SELECT d.name, d.specialization, COUNT(a.appoint_id) AS total_appointments
FROM doctors d
LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id;

SELECT p.medicine, p.dosage
FROM prescriptions p
WHERE p.appoint_id = 1001;

SELECT pr.medicine, pr.dosage, a.date
FROM prescriptions pr
JOIN appointments a ON pr.appoint_id = a.appoint_id
WHERE a.patient_id = 101;

SELECT gender, COUNT(*) FROM patients GROUP BY gender;

SELECT d.name, COUNT(a.appoint_id) AS total
FROM doctors d
JOIN appointments a ON d.doctor_id = a.doctor_id
GROUP BY d.doctor_id
ORDER BY total DESC
LIMIT 1;

SELECT * FROM appointments WHERE date > CURDATE(); 

SELECT * FROM patients WHERE age > 40;

SELECT * FROM patients WHERE name LIKE '%das%';

SELECT * FROM doctors WHERE specialization = 'Cardiologist';

SELECT a.appoint_id, p.name AS patient, d.name AS doctor, a.date, a.problem
FROM appointments a
JOIN patients p ON a.patient_id = p.patient_id
JOIN doctors d ON a.doctor_id = d.doctor_id;

SELECT COUNT(*) FROM prescriptions;

SELECT p.name, a.problem
FROM appointments a
JOIN doctors d ON a.doctor_id = d.doctor_id
JOIN patients p ON a.patient_id = p.patient_id
WHERE d.specialization = 'Dermatologist';

DELETE FROM appointments WHERE appoint_id = 102;

 UPDATE patients SET phone = '9123456780' WHERE patient_id = 101;

SELECT pr.medicine, pr.dosage, p.name AS patient
FROM prescriptions pr
JOIN appointments a ON pr.appoint_id = a.appoint_id
JOIN patients p ON a.patient_id = p.patient_id
WHERE a.doctor_id = 1;

SELECT p.name, COUNT(a.appoint_id) AS total
FROM patients p
LEFT JOIN appointments a ON p.patient_id = a.patient_id
GROUP BY p.patient_id;
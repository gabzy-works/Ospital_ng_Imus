-- MariaDB Hospital Management System Schema
-- This file contains the complete database schema for the hospital system

-- Create database (run this first if database doesn't exist)
-- CREATE DATABASE IF NOT EXISTS hospital_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
-- USE hospital_db;

-- Drop tables if they exist (for clean installation)
DROP TABLE IF EXISTS imports;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS patients;

-- Create patients table
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    lastname VARCHAR(100) NOT NULL,
    firstname VARCHAR(100) NOT NULL,
    middlename VARCHAR(100),
    suffix VARCHAR(20),
    birthday DATE NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(100),
    emergency_contact_name VARCHAR(100),
    emergency_contact_phone VARCHAR(20),
    medical_history TEXT,
    allergies TEXT,
    blood_type VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_new TINYINT(1) DEFAULT 1,
    status VARCHAR(20) DEFAULT 'active',
    
    -- Indexes for better performance
    INDEX idx_name (lastname, firstname, middlename),
    INDEX idx_birthday (birthday),
    INDEX idx_status (status),
    INDEX idx_phone (phone),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create appointments table
CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time TIME DEFAULT '09:00:00',
    type VARCHAR(50) DEFAULT 'Consultation',
    reason TEXT,
    status VARCHAR(20) DEFAULT 'scheduled',
    doctor_name VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraint
    FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
    
    -- Indexes for better performance
    INDEX idx_patient_id (patient_id),
    INDEX idx_appointment_date (appointment_date),
    INDEX idx_status (status),
    INDEX idx_doctor (doctor_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create imports table for tracking data imports
CREATE TABLE imports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    records_imported INT DEFAULT 0,
    import_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'completed',
    
    -- Index for better performance
    INDEX idx_import_date (import_date),
    INDEX idx_import_type (import_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample patients
INSERT INTO patients (lastname, firstname, middlename, suffix, birthday, address, phone, email, emergency_contact_name, emergency_contact_phone, medical_history, allergies, blood_type) VALUES
('Santos', 'Maria', 'Cruz', NULL, '1985-03-15', '123 Rizal St., Imus, Cavite', '09171234567', 'maria.santos@email.com', 'Juan Santos', '09181234567', 'Hypertension', 'None', 'O+'),
('Santos', 'Shayne', 'Cruz', NULL, '1985-05-15', '456 Mabini St., Imus, Cavite', '09172345678', 'shayne.santos@email.com', 'Maria Santos', '09182345678', 'Diabetes Type 2', 'Penicillin', 'A+'),
('Garcia', 'Juan', 'Dela Cruz', 'Jr.', '1990-07-22', '789 Bonifacio Ave., Bacoor, Cavite', '09173456789', 'juan.garcia@email.com', 'Ana Garcia', '09183456789', 'None', 'Shellfish', 'B+'),
('Reyes', 'Ana', 'Bautista', NULL, '1978-11-08', '321 Aguinaldo Hwy., Dasmariñas, Cavite', '09174567890', 'ana.reyes@email.com', 'Pedro Reyes', '09184567890', 'Asthma', 'Dust', 'AB+'),
('Gonzales', 'Pedro', 'Martinez', 'Sr.', '1965-01-30', '654 P. Burgos St., Imus, Cavite', '09175678901', 'pedro.gonzales@email.com', 'Carmen Gonzales', '09185678901', 'Heart Disease', 'None', 'O-'),
('Lopez', 'Carmen', 'Villanueva', NULL, '1992-09-12', '987 Gen. Trias Dr., Gen. Trias, Cavite', '09176789012', 'carmen.lopez@email.com', 'Roberto Lopez', '09186789012', 'None', 'None', 'A-'),
('Mendoza', 'Roberto', 'Fernandez', 'III', '1988-05-18', '159 Molino Blvd., Bacoor, Cavite', '09177890123', 'roberto.mendoza@email.com', 'Luz Mendoza', '09187890123', 'Migraine', 'Aspirin', 'B-'),
('Torres', 'Luz', 'Aquino', NULL, '1975-12-03', '753 Salitran Rd., Dasmariñas, Cavite', '09178901234', 'luz.torres@email.com', 'Miguel Torres', '09188901234', 'Arthritis', 'None', 'AB-'),
('Flores', 'Miguel', 'Ramos', 'Jr.', '1983-08-25', '852 Palico Rd., Imus, Cavite', '09179012345', 'miguel.flores@email.com', 'Rosa Flores', '09189012345', 'None', 'Latex', 'O+'),
('Morales', 'Rosa', 'Castillo', NULL, '1995-04-07', '951 Anabu Rd., Imus, Cavite', '09170123456', 'rosa.morales@email.com', 'Carlos Morales', '09180123456', 'None', 'None', 'A+'),
('Rivera', 'Carlos', 'Jimenez', NULL, '1970-10-14', '357 Tanzang Luma, Imus, Cavite', '09171234560', 'carlos.rivera@email.com', 'Ana Rivera', '09181234560', 'High Blood Pressure', 'Iodine', 'B+');

-- Insert sample appointments
INSERT INTO appointments (patient_id, appointment_date, appointment_time, type, reason, status, doctor_name) VALUES
(1, '2025-02-15', '09:00:00', 'Consultation', 'Regular checkup', 'scheduled', 'Dr. Smith'),
(1, '2025-03-01', '10:30:00', 'Laboratory', 'Blood test', 'scheduled', 'Dr. Johnson'),
(2, '2025-02-20', '14:00:00', 'Follow-up', 'Post-surgery checkup', 'scheduled', 'Dr. Brown'),
(3, '2025-02-25', '11:15:00', 'Imaging', 'X-ray examination', 'scheduled', 'Dr. Davis'),
(4, '2025-03-05', '08:30:00', 'Vaccination', 'Annual flu shot', 'scheduled', 'Dr. Wilson');

-- Create a view for easy patient lookup with appointment counts
CREATE VIEW patient_summary AS
SELECT 
    p.*,
    COUNT(a.id) as appointment_count,
    MAX(a.appointment_date) as last_appointment_date
FROM patients p
LEFT JOIN appointments a ON p.id = a.patient_id
WHERE p.status = 'active'
GROUP BY p.id;

-- Create a view for upcoming appointments
CREATE VIEW upcoming_appointments AS
SELECT 
    a.*,
    CONCAT(p.firstname, ' ', IFNULL(p.middlename, ''), ' ', p.lastname, ' ', IFNULL(p.suffix, '')) as patient_name,
    p.phone as patient_phone,
    p.email as patient_email
FROM appointments a
JOIN patients p ON a.patient_id = p.id
WHERE a.appointment_date >= CURDATE() 
  AND a.status = 'scheduled'
  AND p.status = 'active'
ORDER BY a.appointment_date, a.appointment_time;

-- Show table information
SHOW TABLES;
SELECT 'Database schema created successfully!' as message;
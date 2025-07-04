import sqlite3
from datetime import datetime
import os

def init_database():
    """Initialize the patient database with tables and dummy data"""
    
    # Create database directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Connect to SQLite database
    conn = sqlite3.connect('data/patients.db')
    cursor = conn.cursor()
    
    # Create patients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lastname TEXT NOT NULL,
            firstname TEXT NOT NULL,
            middlename TEXT,
            suffix TEXT,
            birthday DATE NOT NULL,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_new INTEGER DEFAULT 1
        )
    ''')
    
    # Create appointments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            appointment_date DATE NOT NULL,
            type TEXT DEFAULT 'Consultation',
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    # Check if patients table is empty (to avoid duplicate data)
    cursor.execute('SELECT COUNT(*) FROM patients')
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert dummy patient data with IDs
        dummy_patients = [
            (1, 'Santos', 'Maria', 'Cruz', None, '1985-03-15', '123 Rizal St., Imus, Cavite'),
            (2, 'Santos', 'Shayne', 'Cruz', None, '1985-05-15', '456 Mabini St., Imus, Cavite'),
            (3, 'Garcia', 'Juan', 'Dela Cruz', 'Jr.', '1990-07-22', '789 Bonifacio Ave., Bacoor, Cavite'),
            (4, 'Reyes', 'Ana', 'Bautista', None, '1978-11-08', '321 Aguinaldo Hwy., Dasmariñas, Cavite'),
            (5, 'Gonzales', 'Pedro', 'Martinez', 'Sr.', '1965-01-30', '654 P. Burgos St., Imus, Cavite'),
            (6, 'Lopez', 'Carmen', 'Villanueva', None, '1992-09-12', '987 Gen. Trias Dr., Gen. Trias, Cavite'),
            (7, 'Mendoza', 'Roberto', 'Fernandez', 'III', '1988-05-18', '159 Molino Blvd., Bacoor, Cavite'),
            (8, 'Torres', 'Luz', 'Aquino', None, '1975-12-03', '753 Salitran Rd., Dasmariñas, Cavite'),
            (9, 'Flores', 'Miguel', 'Ramos', 'Jr.', '1983-08-25', '852 Palico Rd., Imus, Cavite'),
            (10, 'Morales', 'Rosa', 'Castillo', None, '1995-04-07', '951 Anabu Rd., Imus, Cavite'),
            (11, 'Rivera', 'Carlos', 'Jimenez', None, '1970-10-14', '357 Tanzang Luma, Imus, Cavite')
        ]
        
        cursor.executemany('''
            INSERT INTO patients (id, lastname, firstname, middlename, suffix, birthday, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', dummy_patients)
        
        # Insert some dummy appointments
        dummy_appointments = [
            (1, '2025-02-15', 'Consultation', 'Regular checkup'),
            (1, '2025-03-01', 'Laboratory', 'Blood test'),
            (2, '2025-02-20', 'Follow-up', 'Post-surgery checkup'),
            (3, '2025-02-25', 'Imaging', 'X-ray examination'),
            (4, '2025-03-05', 'Vaccination', 'Annual flu shot'),
        ]
        
        cursor.executemany('''
            INSERT INTO appointments (patient_id, appointment_date, type, reason)
            VALUES (?, ?, ?, ?)
        ''', dummy_appointments)
        
        print(f"Inserted {len(dummy_patients)} dummy patient records")
        print(f"Inserted {len(dummy_appointments)} dummy appointment records")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def add_patient(lastname, firstname, middlename=None, suffix=None, birthday=None, address=None):
    """Add a new patient to the database"""
    try:
        conn = sqlite3.connect('data/patients.db')
        cursor = conn.cursor()
        
        # Insert new patient
        cursor.execute('''
            INSERT INTO patients (lastname, firstname, middlename, suffix, birthday, address, is_new)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        ''', (lastname, firstname, middlename, suffix, birthday, address))
        
        # Get the ID of the newly inserted patient
        patient_id = cursor.lastrowid
        
        # Fetch the complete patient record
        cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
        result = cursor.fetchone()
        
        if result:
            columns = [description[0] for description in cursor.description]
            patient = dict(zip(columns, result))
        else:
            patient = None
            
        conn.commit()
        conn.close()
        
        print(f"Successfully added patient: {firstname} {lastname} (ID: {patient_id})")
        return {'success': True, 'patient': patient, 'patient_id': patient_id}
        
    except Exception as e:
        print(f"Error adding patient: {str(e)}")
        return {'success': False, 'error': str(e)}

def search_patients(lastname=None, firstname=None, middlename=None, suffix=None, birthday=None, address=None):
    """Search for patients based on provided criteria"""
    conn = sqlite3.connect('data/patients.db')
    cursor = conn.cursor()

    # Build dynamic query based on provided parameters
    query = "SELECT * FROM patients WHERE 1=1"
    params = []

    if lastname:
        query += " AND LOWER(TRIM(COALESCE(lastname, ''))) = LOWER(TRIM(?))"
        params.append(lastname)
    if firstname:
        query += " AND LOWER(TRIM(COALESCE(firstname, ''))) = LOWER(TRIM(?))"
        params.append(firstname)
    if middlename:
        query += " AND LOWER(TRIM(COALESCE(middlename, ''))) = LOWER(TRIM(?))"
        params.append(middlename)
    if suffix:
        query += " AND LOWER(TRIM(COALESCE(suffix, ''))) = LOWER(TRIM(?))"
        params.append(suffix)
    if birthday:
        query += " AND TRIM(COALESCE(birthday, '')) = TRIM(?)"
        params.append(birthday)
    if address:
        query += " AND LOWER(TRIM(COALESCE(address, ''))) LIKE LOWER(TRIM(?))"
        params.append(f"%{address}%")

    cursor.execute(query, params)
    results = cursor.fetchall()

    # Convert results to list of dictionaries
    columns = [description[0] for description in cursor.description]
    patients = []
    for row in results:
        patient = dict(zip(columns, row))
        patients.append(patient)

    conn.close()
    return patients

def get_all_patients():
    """Get all patients from the database"""
    
    conn = sqlite3.connect('data/patients.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM patients ORDER BY lastname, firstname")
    results = cursor.fetchall()
    
    # Convert results to list of dictionaries
    columns = [description[0] for description in cursor.description]
    patients = []
    for row in results:
        patient = dict(zip(columns, row))
        patients.append(patient)
    
    conn.close()
    return patients

def get_patient_by_id(patient_id):
    """Get a specific patient by ID"""
    try:
        conn = sqlite3.connect('data/patients.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        result = cursor.fetchone()
        
        if result:
            columns = [description[0] for description in cursor.description]
            patient = dict(zip(columns, result))
        else:
            patient = None
            
        conn.close()
        return patient
        
    except Exception as e:
        print(f"Error getting patient by ID: {str(e)}")
        return None

if __name__ == '__main__':
    # Initialize database when script is run directly
    init_database()
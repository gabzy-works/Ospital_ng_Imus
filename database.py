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
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Check if table is empty (to avoid duplicate data)
    cursor.execute('SELECT COUNT(*) FROM patients')
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert dummy patient data
        dummy_patients = [
            ('Santos', 'Maria', 'Cruz', None, '1985-03-15', '123 Rizal St., Imus, Cavite'),
            ('Santos', 'Shayne', 'Cruz', None, '1985-05-15', '456 Mabini St., Imus, Cavite'),
            ('Garcia', 'Juan', 'Dela Cruz', 'Jr.', '1990-07-22', '789 Bonifacio Ave., Bacoor, Cavite'),
            ('Reyes', 'Ana', 'Bautista', None, '1978-11-08', '321 Aguinaldo Hwy., Dasmariñas, Cavite'),
            ('Gonzales', 'Pedro', 'Martinez', 'Sr.', '1965-01-30', '654 P. Burgos St., Imus, Cavite'),
            ('Lopez', 'Carmen', 'Villanueva', None, '1992-09-12', '987 Gen. Trias Dr., Gen. Trias, Cavite'),
            ('Mendoza', 'Roberto', 'Fernandez', 'III', '1988-05-18', '159 Molino Blvd., Bacoor, Cavite'),
            ('Torres', 'Luz', 'Aquino', None, '1975-12-03', '753 Salitran Rd., Dasmariñas, Cavite'),
            ('Flores', 'Miguel', 'Ramos', 'Jr.', '1983-08-25', '852 Palico Rd., Imus, Cavite'),
            ('Morales', 'Rosa', 'Castillo', None, '1995-04-07', '951 Anabu Rd., Imus, Cavite'),
            ('Rivera', 'Carlos', 'Jimenez', None, '1970-10-14', '357 Tanzang Luma, Imus, Cavite')
        ]
        
        cursor.executemany('''
            INSERT INTO patients (lastname, firstname, middlename, suffix, birthday, address)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', dummy_patients)
        
        print(f"Inserted {len(dummy_patients)} dummy patient records")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

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

if __name__ == '__main__':
    # Initialize database when script is run directly
    init_database()
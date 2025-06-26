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
            ('Santos', 'Maria', 'Cruz', None, '1985-03-15'),
            ('Garcia', 'Juan', 'Dela Cruz', 'Jr.', '1990-07-22'),
            ('Reyes', 'Ana', 'Bautista', None, '1978-11-08'),
            ('Gonzales', 'Pedro', 'Martinez', 'Sr.', '1965-01-30'),
            ('Lopez', 'Carmen', 'Villanueva', None, '1992-09-12'),
            ('Mendoza', 'Roberto', 'Fernandez', 'III', '1988-05-18'),
            ('Torres', 'Luz', 'Aquino', None, '1975-12-03'),
            ('Flores', 'Miguel', 'Ramos', 'Jr.', '1983-08-25'),
            ('Morales', 'Rosa', 'Castillo', None, '1995-04-07'),
            ('Rivera', 'Carlos', 'Jimenez', None, '1970-10-14')
        ]
        
        cursor.executemany('''
            INSERT INTO patients (lastname, firstname, middlename, suffix, birthday)
            VALUES (?, ?, ?, ?, ?)
        ''', dummy_patients)
        
        print(f"Inserted {len(dummy_patients)} dummy patient records")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def search_patients(lastname=None, firstname=None, middlename=None, suffix=None, birthday=None):
    """Search for patients based on provided criteria"""
    
    conn = sqlite3.connect('data/patients.db')
    cursor = conn.cursor()
    
    # Build dynamic query based on provided parameters
    query = "SELECT * FROM patients WHERE 1=1"
    params = []
    
    if lastname:
        query += " AND LOWER(lastname) LIKE LOWER(?)"
        params.append(f"%{lastname}%")
    
    if firstname:
        query += " AND LOWER(firstname) LIKE LOWER(?)"
        params.append(f"%{firstname}%")
    
    if middlename:
        query += " AND LOWER(middlename) LIKE LOWER(?)"
        params.append(f"%{middlename}%")
    
    if suffix:
        query += " AND LOWER(suffix) LIKE LOWER(?)"
        params.append(f"%{suffix}%")
    
    if birthday:
        query += " AND birthday = ?"
        params.append(birthday)
    
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
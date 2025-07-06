import sqlite3
from datetime import datetime
import os
import csv
import json

def init_database():
    """Initialize the patient database with tables and dummy data"""
    
    # Create database directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Connect to SQLite database
    conn = sqlite3.connect('data/patients.db')
    cursor = conn.cursor()
    
    # Create patients table with enhanced fields
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lastname TEXT NOT NULL,
            firstname TEXT NOT NULL,
            middlename TEXT,
            suffix TEXT,
            birthday DATE NOT NULL,
            address TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            emergency_contact_name TEXT,
            emergency_contact_phone TEXT,
            medical_history TEXT,
            allergies TEXT,
            blood_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_new INTEGER DEFAULT 1,
            status TEXT DEFAULT 'active'
        )
    ''')
    
    # Create appointments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            appointment_date DATE NOT NULL,
            appointment_time TIME,
            type TEXT DEFAULT 'Consultation',
            reason TEXT,
            status TEXT DEFAULT 'scheduled',
            doctor_name TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    # Create data_imports table to track imported files
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_imports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            records_imported INTEGER DEFAULT 0,
            import_type TEXT DEFAULT 'csv',
            status TEXT DEFAULT 'completed'
        )
    ''')
    
    # Check if patients table is empty (to avoid duplicate data)
    cursor.execute('SELECT COUNT(*) FROM patients')
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert dummy patient data with enhanced information
        dummy_patients = [
            (1, 'Santos', 'Maria', 'Cruz', None, '1985-03-15', '123 Rizal St., Imus, Cavite', '09171234567', 'maria.santos@email.com', 'Juan Santos', '09181234567', 'Hypertension', 'None', 'O+'),
            (2, 'Santos', 'Shayne', 'Cruz', None, '1985-05-15', '456 Mabini St., Imus, Cavite', '09172345678', 'shayne.santos@email.com', 'Maria Santos', '09182345678', 'Diabetes Type 2', 'Penicillin', 'A+'),
            (3, 'Garcia', 'Juan', 'Dela Cruz', 'Jr.', '1990-07-22', '789 Bonifacio Ave., Bacoor, Cavite', '09173456789', 'juan.garcia@email.com', 'Ana Garcia', '09183456789', 'None', 'Shellfish', 'B+'),
            (4, 'Reyes', 'Ana', 'Bautista', None, '1978-11-08', '321 Aguinaldo Hwy., Dasmariñas, Cavite', '09174567890', 'ana.reyes@email.com', 'Pedro Reyes', '09184567890', 'Asthma', 'Dust', 'AB+'),
            (5, 'Gonzales', 'Pedro', 'Martinez', 'Sr.', '1965-01-30', '654 P. Burgos St., Imus, Cavite', '09175678901', 'pedro.gonzales@email.com', 'Carmen Gonzales', '09185678901', 'Heart Disease', 'None', 'O-'),
            (6, 'Lopez', 'Carmen', 'Villanueva', None, '1992-09-12', '987 Gen. Trias Dr., Gen. Trias, Cavite', '09176789012', 'carmen.lopez@email.com', 'Roberto Lopez', '09186789012', 'None', 'None', 'A-'),
            (7, 'Mendoza', 'Roberto', 'Fernandez', 'III', '1988-05-18', '159 Molino Blvd., Bacoor, Cavite', '09177890123', 'roberto.mendoza@email.com', 'Luz Mendoza', '09187890123', 'Migraine', 'Aspirin', 'B-'),
            (8, 'Torres', 'Luz', 'Aquino', None, '1975-12-03', '753 Salitran Rd., Dasmariñas, Cavite', '09178901234', 'luz.torres@email.com', 'Miguel Torres', '09188901234', 'Arthritis', 'None', 'AB-'),
            (9, 'Flores', 'Miguel', 'Ramos', 'Jr.', '1983-08-25', '852 Palico Rd., Imus, Cavite', '09179012345', 'miguel.flores@email.com', 'Rosa Flores', '09189012345', 'None', 'Latex', 'O+'),
            (10, 'Morales', 'Rosa', 'Castillo', None, '1995-04-07', '951 Anabu Rd., Imus, Cavite', '09170123456', 'rosa.morales@email.com', 'Carlos Morales', '09180123456', 'None', 'None', 'A+'),
            (11, 'Rivera', 'Carlos', 'Jimenez', None, '1970-10-14', '357 Tanzang Luma, Imus, Cavite', '09171234560', 'carlos.rivera@email.com', 'Ana Rivera', '09181234560', 'High Blood Pressure', 'Iodine', 'B+')
        ]
        
        cursor.executemany('''
            INSERT INTO patients (id, lastname, firstname, middlename, suffix, birthday, address, phone, email, emergency_contact_name, emergency_contact_phone, medical_history, allergies, blood_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', dummy_patients)
        
        # Insert some dummy appointments
        dummy_appointments = [
            (1, '2025-02-15', '09:00', 'Consultation', 'Regular checkup', 'scheduled', 'Dr. Smith', ''),
            (1, '2025-03-01', '10:30', 'Laboratory', 'Blood test', 'scheduled', 'Dr. Johnson', ''),
            (2, '2025-02-20', '14:00', 'Follow-up', 'Post-surgery checkup', 'scheduled', 'Dr. Brown', ''),
            (3, '2025-02-25', '11:15', 'Imaging', 'X-ray examination', 'scheduled', 'Dr. Davis', ''),
            (4, '2025-03-05', '08:30', 'Vaccination', 'Annual flu shot', 'scheduled', 'Dr. Wilson', ''),
        ]
        
        cursor.executemany('''
            INSERT INTO appointments (patient_id, appointment_date, appointment_time, type, reason, status, doctor_name, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', dummy_appointments)
        
        print(f"Inserted {len(dummy_patients)} dummy patient records")
        print(f"Inserted {len(dummy_appointments)} dummy appointment records")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def add_patient(lastname, firstname, middlename=None, suffix=None, birthday=None, address=None, 
                phone=None, email=None, emergency_contact_name=None, emergency_contact_phone=None,
                medical_history=None, allergies=None, blood_type=None):
    """Add a new patient to the database with enhanced fields"""
    try:
        conn = sqlite3.connect('data/patients.db')
        cursor = conn.cursor()
        
        # Insert new patient
        cursor.execute('''
            INSERT INTO patients (lastname, firstname, middlename, suffix, birthday, address, 
                                phone, email, emergency_contact_name, emergency_contact_phone,
                                medical_history, allergies, blood_type, is_new)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        ''', (lastname, firstname, middlename, suffix, birthday, address, 
              phone, email, emergency_contact_name, emergency_contact_phone,
              medical_history, allergies, blood_type))
        
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

def import_patients_from_csv(file_path):
    """Import patients from a CSV file"""
    try:
        conn = sqlite3.connect('data/patients.db')
        cursor = conn.cursor()
        
        imported_count = 0
        errors = []
        
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            # Try to detect the delimiter
            sample = csvfile.read(1024)
            csvfile.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 because row 1 is header
                try:
                    # Map CSV columns to database fields (flexible mapping)
                    patient_data = {
                        'lastname': row.get('lastname') or row.get('last_name') or row.get('LastName') or '',
                        'firstname': row.get('firstname') or row.get('first_name') or row.get('FirstName') or '',
                        'middlename': row.get('middlename') or row.get('middle_name') or row.get('MiddleName') or None,
                        'suffix': row.get('suffix') or row.get('Suffix') or None,
                        'birthday': row.get('birthday') or row.get('birth_date') or row.get('date_of_birth') or row.get('Birthday') or '',
                        'address': row.get('address') or row.get('Address') or '',
                        'phone': row.get('phone') or row.get('phone_number') or row.get('Phone') or None,
                        'email': row.get('email') or row.get('Email') or None,
                        'emergency_contact_name': row.get('emergency_contact_name') or row.get('emergency_contact') or None,
                        'emergency_contact_phone': row.get('emergency_contact_phone') or row.get('emergency_phone') or None,
                        'medical_history': row.get('medical_history') or row.get('Medical_History') or None,
                        'allergies': row.get('allergies') or row.get('Allergies') or None,
                        'blood_type': row.get('blood_type') or row.get('Blood_Type') or None
                    }
                    
                    # Validate required fields
                    if not patient_data['lastname'] or not patient_data['firstname'] or not patient_data['birthday'] or not patient_data['address']:
                        errors.append(f"Row {row_num}: Missing required fields (lastname, firstname, birthday, address)")
                        continue
                    
                    # Check if patient already exists
                    cursor.execute('''
                        SELECT id FROM patients 
                        WHERE LOWER(lastname) = LOWER(?) AND LOWER(firstname) = LOWER(?) 
                        AND LOWER(COALESCE(middlename, '')) = LOWER(COALESCE(?, '')) 
                        AND birthday = ?
                    ''', (patient_data['lastname'], patient_data['firstname'], 
                          patient_data['middlename'], patient_data['birthday']))
                    
                    if cursor.fetchone():
                        errors.append(f"Row {row_num}: Patient already exists")
                        continue
                    
                    # Insert patient
                    cursor.execute('''
                        INSERT INTO patients (lastname, firstname, middlename, suffix, birthday, address,
                                            phone, email, emergency_contact_name, emergency_contact_phone,
                                            medical_history, allergies, blood_type, is_new)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                    ''', (patient_data['lastname'], patient_data['firstname'], patient_data['middlename'],
                          patient_data['suffix'], patient_data['birthday'], patient_data['address'],
                          patient_data['phone'], patient_data['email'], patient_data['emergency_contact_name'],
                          patient_data['emergency_contact_phone'], patient_data['medical_history'],
                          patient_data['allergies'], patient_data['blood_type']))
                    
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
        
        # Record the import
        cursor.execute('''
            INSERT INTO data_imports (filename, records_imported, import_type)
            VALUES (?, ?, 'csv')
        ''', (os.path.basename(file_path), imported_count))
        
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'imported_count': imported_count,
            'errors': errors,
            'total_errors': len(errors)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'imported_count': 0,
            'errors': []
        }

def import_patients_from_json(file_path):
    """Import patients from a JSON file"""
    try:
        conn = sqlite3.connect('data/patients.db')
        cursor = conn.cursor()
        
        imported_count = 0
        errors = []
        
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            
            # Handle different JSON structures
            if isinstance(data, list):
                patients_data = data
            elif isinstance(data, dict) and 'patients' in data:
                patients_data = data['patients']
            else:
                return {'success': False, 'error': 'Invalid JSON structure'}
            
            for index, patient in enumerate(patients_data):
                try:
                    # Validate required fields
                    required_fields = ['lastname', 'firstname', 'birthday', 'address']
                    missing_fields = [field for field in required_fields if not patient.get(field)]
                    
                    if missing_fields:
                        errors.append(f"Patient {index + 1}: Missing required fields: {', '.join(missing_fields)}")
                        continue
                    
                    # Check if patient already exists
                    cursor.execute('''
                        SELECT id FROM patients 
                        WHERE LOWER(lastname) = LOWER(?) AND LOWER(firstname) = LOWER(?) 
                        AND LOWER(COALESCE(middlename, '')) = LOWER(COALESCE(?, '')) 
                        AND birthday = ?
                    ''', (patient['lastname'], patient['firstname'], 
                          patient.get('middlename'), patient['birthday']))
                    
                    if cursor.fetchone():
                        errors.append(f"Patient {index + 1}: Already exists")
                        continue
                    
                    # Insert patient
                    cursor.execute('''
                        INSERT INTO patients (lastname, firstname, middlename, suffix, birthday, address,
                                            phone, email, emergency_contact_name, emergency_contact_phone,
                                            medical_history, allergies, blood_type, is_new)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                    ''', (patient['lastname'], patient['firstname'], patient.get('middlename'),
                          patient.get('suffix'), patient['birthday'], patient['address'],
                          patient.get('phone'), patient.get('email'), patient.get('emergency_contact_name'),
                          patient.get('emergency_contact_phone'), patient.get('medical_history'),
                          patient.get('allergies'), patient.get('blood_type')))
                    
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Patient {index + 1}: {str(e)}")
        
        # Record the import
        cursor.execute('''
            INSERT INTO data_imports (filename, records_imported, import_type)
            VALUES (?, ?, 'json')
        ''', (os.path.basename(file_path), imported_count))
        
        conn.commit()
        conn.close()
        
        return {
            'success': True,
            'imported_count': imported_count,
            'errors': errors,
            'total_errors': len(errors)
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'imported_count': 0,
            'errors': []
        }

def search_patients(lastname=None, firstname=None, middlename=None, suffix=None, birthday=None, address=None):
    """Search for patients based on provided criteria"""
    conn = sqlite3.connect('data/patients.db')
    cursor = conn.cursor()

    # Build dynamic query based on provided parameters
    query = "SELECT * FROM patients WHERE status = 'active'"
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
    """Get all active patients from the database"""
    
    conn = sqlite3.connect('data/patients.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM patients WHERE status = 'active' ORDER BY lastname, firstname")
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
        
        cursor.execute("SELECT * FROM patients WHERE id = ? AND status = 'active'", (patient_id,))
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

def get_import_history():
    """Get the history of data imports"""
    try:
        conn = sqlite3.connect('data/patients.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM data_imports ORDER BY import_date DESC")
        results = cursor.fetchall()
        
        columns = [description[0] for description in cursor.description]
        imports = []
        for row in results:
            import_record = dict(zip(columns, row))
            imports.append(import_record)
        
        conn.close()
        return imports
        
    except Exception as e:
        print(f"Error getting import history: {str(e)}")
        return []

if __name__ == '__main__':
    # Initialize database when script is run directly
    init_database()
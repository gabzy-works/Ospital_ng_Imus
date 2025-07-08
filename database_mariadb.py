import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'hospital_db'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci',
    'autocommit': True
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return None

def init_database():
    """Initialize the database with required tables and sample data"""
    connection = get_db_connection()
    if not connection:
        print("Failed to connect to database")
        return False
    
    try:
        cursor = connection.cursor()
        
        # Create patients table
        create_patients_table = """
        CREATE TABLE IF NOT EXISTS patients (
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
            INDEX idx_name (lastname, firstname, middlename),
            INDEX idx_birthday (birthday),
            INDEX idx_status (status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        # Create appointments table
        create_appointments_table = """
        CREATE TABLE IF NOT EXISTS appointments (
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
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
            INDEX idx_patient_id (patient_id),
            INDEX idx_appointment_date (appointment_date),
            INDEX idx_status (status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        # Create imports table
        create_imports_table = """
        CREATE TABLE IF NOT EXISTS imports (
            id INT AUTO_INCREMENT PRIMARY KEY,
            filename VARCHAR(255) NOT NULL,
            import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            records_imported INT DEFAULT 0,
            import_type VARCHAR(20) NOT NULL,
            status VARCHAR(20) DEFAULT 'completed'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        cursor.execute(create_patients_table)
        cursor.execute(create_appointments_table)
        cursor.execute(create_imports_table)
        
        # Check if patients table is empty and insert sample data
        cursor.execute("SELECT COUNT(*) FROM patients")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Insert sample patients
            sample_patients = [
                ('Santos', 'Maria', 'Cruz', None, '1985-03-15', '123 Rizal St., Imus, Cavite', '09171234567', 'maria.santos@email.com', 'Juan Santos', '09181234567', 'Hypertension', 'None', 'O+'),
                ('Santos', 'Shayne', 'Cruz', None, '1985-05-15', '456 Mabini St., Imus, Cavite', '09172345678', 'shayne.santos@email.com', 'Maria Santos', '09182345678', 'Diabetes Type 2', 'Penicillin', 'A+'),
                ('Garcia', 'Juan', 'Dela Cruz', 'Jr.', '1990-07-22', '789 Bonifacio Ave., Bacoor, Cavite', '09173456789', 'juan.garcia@email.com', 'Ana Garcia', '09183456789', 'None', 'Shellfish', 'B+'),
                ('Reyes', 'Ana', 'Bautista', None, '1978-11-08', '321 Aguinaldo Hwy., Dasmariñas, Cavite', '09174567890', 'ana.reyes@email.com', 'Pedro Reyes', '09184567890', 'Asthma', 'Dust', 'AB+'),
                ('Gonzales', 'Pedro', 'Martinez', 'Sr.', '1965-01-30', '654 P. Burgos St., Imus, Cavite', '09175678901', 'pedro.gonzales@email.com', 'Carmen Gonzales', '09185678901', 'Heart Disease', 'None', 'O-'),
                ('Lopez', 'Carmen', 'Villanueva', None, '1992-09-12', '987 Gen. Trias Dr., Gen. Trias, Cavite', '09176789012', 'carmen.lopez@email.com', 'Roberto Lopez', '09186789012', 'None', 'None', 'A-'),
                ('Mendoza', 'Roberto', 'Fernandez', 'III', '1988-05-18', '159 Molino Blvd., Bacoor, Cavite', '09177890123', 'roberto.mendoza@email.com', 'Luz Mendoza', '09187890123', 'Migraine', 'Aspirin', 'B-'),
                ('Torres', 'Luz', 'Aquino', None, '1975-12-03', '753 Salitran Rd., Dasmariñas, Cavite', '09178901234', 'luz.torres@email.com', 'Miguel Torres', '09188901234', 'Arthritis', 'None', 'AB-'),
                ('Flores', 'Miguel', 'Ramos', 'Jr.', '1983-08-25', '852 Palico Rd., Imus, Cavite', '09179012345', 'miguel.flores@email.com', 'Rosa Flores', '09189012345', 'None', 'Latex', 'O+'),
                ('Morales', 'Rosa', 'Castillo', None, '1995-04-07', '951 Anabu Rd., Imus, Cavite', '09170123456', 'rosa.morales@email.com', 'Carlos Morales', '09180123456', 'None', 'None', 'A+'),
                ('Rivera', 'Carlos', 'Jimenez', None, '1970-10-14', '357 Tanzang Luma, Imus, Cavite', '09171234560', 'carlos.rivera@email.com', 'Ana Rivera', '09181234560', 'High Blood Pressure', 'Iodine', 'B+')
            ]
            
            insert_patient_query = """
            INSERT INTO patients (lastname, firstname, middlename, suffix, birthday, address, phone, email, 
                                emergency_contact_name, emergency_contact_phone, medical_history, allergies, blood_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.executemany(insert_patient_query, sample_patients)
            print(f"Inserted {len(sample_patients)} sample patients")
            
            # Insert sample appointments
            sample_appointments = [
                (1, '2025-02-15', '09:00:00', 'Consultation', 'Regular checkup', 'scheduled', 'Dr. Smith'),
                (1, '2025-03-01', '10:30:00', 'Laboratory', 'Blood test', 'scheduled', 'Dr. Johnson'),
                (2, '2025-02-20', '14:00:00', 'Follow-up', 'Post-surgery checkup', 'scheduled', 'Dr. Brown'),
                (3, '2025-02-25', '11:15:00', 'Imaging', 'X-ray examination', 'scheduled', 'Dr. Davis'),
                (4, '2025-03-05', '08:30:00', 'Vaccination', 'Annual flu shot', 'scheduled', 'Dr. Wilson')
            ]
            
            insert_appointment_query = """
            INSERT INTO appointments (patient_id, appointment_date, appointment_time, type, reason, status, doctor_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            cursor.executemany(insert_appointment_query, sample_appointments)
            print(f"Inserted {len(sample_appointments)} sample appointments")
        
        connection.commit()
        print("Database initialized successfully!")
        return True
        
    except Error as e:
        print(f"Error initializing database: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def search_patients(lastname=None, firstname=None, middlename=None, suffix=None, birthday=None, address=None):
    """Search for patients based on provided criteria"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Build dynamic query
        query = "SELECT * FROM patients WHERE status = 'active'"
        params = []
        
        if lastname:
            query += " AND lastname = %s"
            params.append(lastname)
        if firstname:
            query += " AND firstname = %s"
            params.append(firstname)
        if middlename:
            query += " AND middlename = %s"
            params.append(middlename)
        if suffix:
            query += " AND suffix = %s"
            params.append(suffix)
        if birthday:
            query += " AND birthday = %s"
            params.append(birthday)
        if address:
            query += " AND address LIKE %s"
            params.append(f"%{address}%")
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        # Convert datetime objects to strings for JSON serialization
        for result in results:
            if result.get('birthday'):
                result['birthday'] = result['birthday'].strftime('%Y-%m-%d')
            if result.get('created_at'):
                result['created_at'] = result['created_at'].isoformat()
            if result.get('updated_at'):
                result['updated_at'] = result['updated_at'].isoformat()
        
        return results
        
    except Error as e:
        print(f"Error searching patients: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_all_patients():
    """Get all active patients from the database"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients WHERE status = 'active' ORDER BY lastname, firstname")
        results = cursor.fetchall()
        
        # Convert datetime objects to strings
        for result in results:
            if result.get('birthday'):
                result['birthday'] = result['birthday'].strftime('%Y-%m-%d')
            if result.get('created_at'):
                result['created_at'] = result['created_at'].isoformat()
            if result.get('updated_at'):
                result['updated_at'] = result['updated_at'].isoformat()
        
        return results
        
    except Error as e:
        print(f"Error getting all patients: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_patient_by_id(patient_id):
    """Get a specific patient by ID"""
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients WHERE id = %s AND status = 'active'", (patient_id,))
        result = cursor.fetchone()
        
        if result:
            if result.get('birthday'):
                result['birthday'] = result['birthday'].strftime('%Y-%m-%d')
            if result.get('created_at'):
                result['created_at'] = result['created_at'].isoformat()
            if result.get('updated_at'):
                result['updated_at'] = result['updated_at'].isoformat()
        
        return result
        
    except Error as e:
        print(f"Error getting patient by ID: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def add_patient(lastname, firstname, middlename=None, suffix=None, birthday=None, address=None, 
                phone=None, email=None, emergency_contact_name=None, emergency_contact_phone=None,
                medical_history=None, allergies=None, blood_type=None):
    """Add a new patient to the database"""
    connection = get_db_connection()
    if not connection:
        return {'success': False, 'error': 'Database connection failed'}
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = """
        INSERT INTO patients (lastname, firstname, middlename, suffix, birthday, address, phone, email,
                            emergency_contact_name, emergency_contact_phone, medical_history, allergies, blood_type)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        params = (lastname, firstname, middlename, suffix, birthday, address, phone, email,
                 emergency_contact_name, emergency_contact_phone, medical_history, allergies, blood_type)
        
        cursor.execute(query, params)
        patient_id = cursor.lastrowid
        
        # Get the created patient
        cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
        patient = cursor.fetchone()
        
        if patient:
            if patient.get('birthday'):
                patient['birthday'] = patient['birthday'].strftime('%Y-%m-%d')
            if patient.get('created_at'):
                patient['created_at'] = patient['created_at'].isoformat()
            if patient.get('updated_at'):
                patient['updated_at'] = patient['updated_at'].isoformat()
        
        connection.commit()
        return {'success': True, 'patient': patient, 'patient_id': patient_id}
        
    except Error as e:
        print(f"Error adding patient: {e}")
        return {'success': False, 'error': str(e)}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_appointments_by_patient_id(patient_id):
    """Get all appointments for a specific patient"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM appointments 
            WHERE patient_id = %s 
            ORDER BY appointment_date DESC
        """, (patient_id,))
        results = cursor.fetchall()
        
        # Convert datetime objects to strings
        for result in results:
            if result.get('appointment_date'):
                result['appointment_date'] = result['appointment_date'].strftime('%Y-%m-%d')
            if result.get('appointment_time'):
                result['appointment_time'] = str(result['appointment_time'])
            if result.get('created_at'):
                result['created_at'] = result['created_at'].isoformat()
        
        return results
        
    except Error as e:
        print(f"Error getting appointments: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def create_appointment(patient_id, appointment_date, appointment_time='09:00', appointment_type='Consultation', 
                      reason='', doctor_name=''):
    """Create a new appointment for a patient"""
    connection = get_db_connection()
    if not connection:
        return {'success': False, 'error': 'Database connection failed'}
    
    try:
        cursor = connection.cursor()
        
        query = """
        INSERT INTO appointments (patient_id, appointment_date, appointment_time, type, reason, doctor_name)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        params = (patient_id, appointment_date, appointment_time, appointment_type, reason, doctor_name)
        cursor.execute(query, params)
        appointment_id = cursor.lastrowid
        
        connection.commit()
        return {'success': True, 'appointment_id': appointment_id}
        
    except Error as e:
        print(f"Error creating appointment: {e}")
        return {'success': False, 'error': str(e)}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_all_appointments():
    """Get all appointments with patient information"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT a.*, 
                   CONCAT(p.firstname, ' ', IFNULL(p.middlename, ''), ' ', p.lastname, ' ', IFNULL(p.suffix, '')) as patient_name
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            WHERE p.status = 'active'
            ORDER BY a.appointment_date DESC
        """)
        results = cursor.fetchall()
        
        # Convert datetime objects to strings
        for result in results:
            if result.get('appointment_date'):
                result['appointment_date'] = result['appointment_date'].strftime('%Y-%m-%d')
            if result.get('appointment_time'):
                result['appointment_time'] = str(result['appointment_time'])
            if result.get('created_at'):
                result['created_at'] = result['created_at'].isoformat()
            # Clean up patient name
            result['patient_name'] = ' '.join(result['patient_name'].split())
        
        return results
        
    except Error as e:
        print(f"Error getting all appointments: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_import_history():
    """Get the history of data imports"""
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM imports ORDER BY import_date DESC")
        results = cursor.fetchall()
        
        # Convert datetime objects to strings
        for result in results:
            if result.get('import_date'):
                result['import_date'] = result['import_date'].isoformat()
        
        return results
        
    except Error as e:
        print(f"Error getting import history: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def import_patients_from_csv(file_path):
    """Import patients from a CSV file"""
    import csv
    
    connection = get_db_connection()
    if not connection:
        return {'success': False, 'error': 'Database connection failed', 'imported_count': 0, 'errors': []}
    
    try:
        cursor = connection.cursor(dictionary=True)
        imported_count = 0
        errors = []
        
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            # Try to detect the delimiter
            sample = csvfile.read(1024)
            csvfile.seek(0)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            
            reader = csv.DictReader(csvfile, delimiter=delimiter)
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    # Map CSV columns to database fields
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
                        errors.append(f"Row {row_num}: Missing required fields")
                        continue
                    
                    # Check if patient already exists
                    cursor.execute("""
                        SELECT id FROM patients 
                        WHERE lastname = %s AND firstname = %s AND middlename = %s AND birthday = %s
                    """, (patient_data['lastname'], patient_data['firstname'], patient_data['middlename'], patient_data['birthday']))
                    
                    if cursor.fetchone():
                        errors.append(f"Row {row_num}: Patient already exists")
                        continue
                    
                    # Insert new patient
                    insert_query = """
                    INSERT INTO patients (lastname, firstname, middlename, suffix, birthday, address, phone, email,
                                        emergency_contact_name, emergency_contact_phone, medical_history, allergies, blood_type, is_new)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0)
                    """
                    
                    cursor.execute(insert_query, (
                        patient_data['lastname'], patient_data['firstname'], patient_data['middlename'],
                        patient_data['suffix'], patient_data['birthday'], patient_data['address'],
                        patient_data['phone'], patient_data['email'], patient_data['emergency_contact_name'],
                        patient_data['emergency_contact_phone'], patient_data['medical_history'],
                        patient_data['allergies'], patient_data['blood_type']
                    ))
                    
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
        
        # Record the import
        cursor.execute("""
            INSERT INTO imports (filename, records_imported, import_type)
            VALUES (%s, %s, 'csv')
        """, (os.path.basename(file_path), imported_count))
        
        connection.commit()
        
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
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def import_patients_from_json(file_path):
    """Import patients from a JSON file"""
    import json
    
    connection = get_db_connection()
    if not connection:
        return {'success': False, 'error': 'Database connection failed', 'imported_count': 0, 'errors': []}
    
    try:
        cursor = connection.cursor(dictionary=True)
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
                    cursor.execute("""
                        SELECT id FROM patients 
                        WHERE lastname = %s AND firstname = %s AND middlename = %s AND birthday = %s
                    """, (patient['lastname'], patient['firstname'], patient.get('middlename'), patient['birthday']))
                    
                    if cursor.fetchone():
                        errors.append(f"Patient {index + 1}: Already exists")
                        continue
                    
                    # Insert new patient
                    insert_query = """
                    INSERT INTO patients (lastname, firstname, middlename, suffix, birthday, address, phone, email,
                                        emergency_contact_name, emergency_contact_phone, medical_history, allergies, blood_type, is_new)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0)
                    """
                    
                    cursor.execute(insert_query, (
                        patient['lastname'], patient['firstname'], patient.get('middlename'),
                        patient.get('suffix'), patient['birthday'], patient['address'],
                        patient.get('phone'), patient.get('email'), patient.get('emergency_contact_name'),
                        patient.get('emergency_contact_phone'), patient.get('medical_history'),
                        patient.get('allergies'), patient.get('blood_type')
                    ))
                    
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Patient {index + 1}: {str(e)}")
        
        # Record the import
        cursor.execute("""
            INSERT INTO imports (filename, records_imported, import_type)
            VALUES (%s, %s, 'json')
        """, (os.path.basename(file_path), imported_count))
        
        connection.commit()
        
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
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    # Test database connection and initialization
    print("Testing MariaDB connection...")
    if init_database():
        print("Database connection and initialization successful!")
    else:
        print("Database connection failed!")
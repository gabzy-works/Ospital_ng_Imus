import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any

# File paths for JSON storage
DATA_DIR = 'data'
PATIENTS_FILE = os.path.join(DATA_DIR, 'patients.json')
APPOINTMENTS_FILE = os.path.join(DATA_DIR, 'appointments.json')
IMPORTS_FILE = os.path.join(DATA_DIR, 'imports.json')

def ensure_data_directory():
    """Ensure the data directory exists"""
    os.makedirs(DATA_DIR, exist_ok=True)

def load_json_file(filepath: str, default_data: Any = None) -> Any:
    """Load data from a JSON file"""
    if default_data is None:
        default_data = []
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return default_data
    except (json.JSONDecodeError, IOError):
        return default_data

def save_json_file(filepath: str, data: Any) -> bool:
    """Save data to a JSON file"""
    try:
        ensure_data_directory()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False

def get_next_id(data_list: List[Dict]) -> int:
    """Get the next available ID for a list of records"""
    if not data_list:
        return 1
    return max(item.get('id', 0) for item in data_list) + 1

def init_database():
    """Initialize the patient database with JSON files and dummy data"""
    ensure_data_directory()
    
    # Load existing data
    patients = load_json_file(PATIENTS_FILE, [])
    appointments = load_json_file(APPOINTMENTS_FILE, [])
    imports = load_json_file(IMPORTS_FILE, [])
    
    # If patients file is empty, add dummy data
    if not patients:
        dummy_patients = [
            {
                'id': 1, 'lastname': 'Santos', 'firstname': 'Maria', 'middlename': 'Cruz', 'suffix': None,
                'birthday': '1985-03-15', 'address': '123 Rizal St., Imus, Cavite', 'phone': '09171234567',
                'email': 'maria.santos@email.com', 'emergency_contact_name': 'Juan Santos',
                'emergency_contact_phone': '09181234567', 'medical_history': 'Hypertension',
                'allergies': 'None', 'blood_type': 'O+', 'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(), 'is_new': 1, 'status': 'active'
            },
            {
                'id': 2, 'lastname': 'Santos', 'firstname': 'Shayne', 'middlename': 'Cruz', 'suffix': None,
                'birthday': '1985-05-15', 'address': '456 Mabini St., Imus, Cavite', 'phone': '09172345678',
                'email': 'shayne.santos@email.com', 'emergency_contact_name': 'Maria Santos',
                'emergency_contact_phone': '09182345678', 'medical_history': 'Diabetes Type 2',
                'allergies': 'Penicillin', 'blood_type': 'A+', 'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(), 'is_new': 1, 'status': 'active'
            },
            {
                'id': 3, 'lastname': 'Garcia', 'firstname': 'Juan', 'middlename': 'Dela Cruz', 'suffix': 'Jr.',
                'birthday': '1990-07-22', 'address': '789 Bonifacio Ave., Bacoor, Cavite', 'phone': '09173456789',
                'email': 'juan.garcia@email.com', 'emergency_contact_name': 'Ana Garcia',
                'emergency_contact_phone': '09183456789', 'medical_history': 'None',
                'allergies': 'Shellfish', 'blood_type': 'B+', 'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(), 'is_new': 1, 'status': 'active'
            },
            {
                'id': 4, 'lastname': 'Reyes', 'firstname': 'Ana', 'middlename': 'Bautista', 'suffix': None,
                'birthday': '1978-11-08', 'address': '321 Aguinaldo Hwy., Dasmariñas, Cavite', 'phone': '09174567890',
                'email': 'ana.reyes@email.com', 'emergency_contact_name': 'Pedro Reyes',
                'emergency_contact_phone': '09184567890', 'medical_history': 'Asthma',
                'allergies': 'Dust', 'blood_type': 'AB+', 'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(), 'is_new': 1, 'status': 'active'
            },
            {
                'id': 5, 'lastname': 'Gonzales', 'firstname': 'Pedro', 'middlename': 'Martinez', 'suffix': 'Sr.',
                'birthday': '1965-01-30', 'address': '654 P. Burgos St., Imus, Cavite', 'phone': '09175678901',
                'email': 'pedro.gonzales@email.com', 'emergency_contact_name': 'Carmen Gonzales',
                'emergency_contact_phone': '09185678901', 'medical_history': 'Heart Disease',
                'allergies': 'None', 'blood_type': 'O-', 'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(), 'is_new': 1, 'status': 'active'
            },
            {
                'id': 6, 'lastname': 'Lopez', 'firstname': 'Carmen', 'middlename': 'Villanueva', 'suffix': None,
                'birthday': '1992-09-12', 'address': '987 Gen. Trias Dr., Gen. Trias, Cavite', 'phone': '09176789012',
                'email': 'carmen.lopez@email.com', 'emergency_contact_name': 'Roberto Lopez',
                'emergency_contact_phone': '09186789012', 'medical_history': 'None',
                'allergies': 'None', 'blood_type': 'A-', 'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(), 'is_new': 1, 'status': 'active'
            },
            {
                'id': 7, 'lastname': 'Mendoza', 'firstname': 'Roberto', 'middlename': 'Fernandez', 'suffix': 'III',
                'birthday': '1988-05-18', 'address': '159 Molino Blvd., Bacoor, Cavite', 'phone': '09177890123',
                'email': 'roberto.mendoza@email.com', 'emergency_contact_name': 'Luz Mendoza',
                'emergency_contact_phone': '09187890123', 'medical_history': 'Migraine',
                'allergies': 'Aspirin', 'blood_type': 'B-', 'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(), 'is_new': 1, 'status': 'active'
            },
            {
                'id': 8, 'lastname': 'Torres', 'firstname': 'Luz', 'middlename': 'Aquino', 'suffix': None,
                'birthday': '1975-12-03', 'address': '753 Salitran Rd., Dasmariñas, Cavite', 'phone': '09178901234',
                'email': 'luz.torres@email.com', 'emergency_contact_name': 'Miguel Torres',
                'emergency_contact_phone': '09188901234', 'medical_history': 'Arthritis',
                'allergies': 'None', 'blood_type': 'AB-', 'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(), 'is_new': 1, 'status': 'active'
            },
            {
                'id': 9, 'lastname': 'Flores', 'firstname': 'Miguel', 'middlename': 'Ramos', 'suffix': 'Jr.',
                'birthday': '1983-08-25', 'address': '852 Palico Rd., Imus, Cavite', 'phone': '09179012345',
                'email': 'miguel.flores@email.com', 'emergency_contact_name': 'Rosa Flores',
                'emergency_contact_phone': '09189012345', 'medical_history': 'None',
                'allergies': 'Latex', 'blood_type': 'O+', 'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(), 'is_new': 1, 'status': 'active'
            },
            {
                'id': 10, 'lastname': 'Morales', 'firstname': 'Rosa', 'middlename': 'Castillo', 'suffix': None,
                'birthday': '1995-04-07', 'address': '951 Anabu Rd., Imus, Cavite', 'phone': '09170123456',
                'email': 'rosa.morales@email.com', 'emergency_contact_name': 'Carlos Morales',
                'emergency_contact_phone': '09180123456', 'medical_history': 'None',
                'allergies': 'None', 'blood_type': 'A+', 'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(), 'is_new': 1, 'status': 'active'
            },
            {
                'id': 11, 'lastname': 'Rivera', 'firstname': 'Carlos', 'middlename': 'Jimenez', 'suffix': None,
                'birthday': '1970-10-14', 'address': '357 Tanzang Luma, Imus, Cavite', 'phone': '09171234560',
                'email': 'carlos.rivera@email.com', 'emergency_contact_name': 'Ana Rivera',
                'emergency_contact_phone': '09181234560', 'medical_history': 'High Blood Pressure',
                'allergies': 'Iodine', 'blood_type': 'B+', 'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(), 'is_new': 1, 'status': 'active'
            }
        ]
        
        save_json_file(PATIENTS_FILE, dummy_patients)
        print(f"Inserted {len(dummy_patients)} dummy patient records")
    
    # If appointments file is empty, add dummy data
    if not appointments:
        dummy_appointments = [
            {
                'id': 1, 'patient_id': 1, 'appointment_date': '2025-02-15', 'appointment_time': '09:00',
                'type': 'Consultation', 'reason': 'Regular checkup', 'status': 'scheduled',
                'doctor_name': 'Dr. Smith', 'notes': '', 'created_at': datetime.now().isoformat()
            },
            {
                'id': 2, 'patient_id': 1, 'appointment_date': '2025-03-01', 'appointment_time': '10:30',
                'type': 'Laboratory', 'reason': 'Blood test', 'status': 'scheduled',
                'doctor_name': 'Dr. Johnson', 'notes': '', 'created_at': datetime.now().isoformat()
            },
            {
                'id': 3, 'patient_id': 2, 'appointment_date': '2025-02-20', 'appointment_time': '14:00',
                'type': 'Follow-up', 'reason': 'Post-surgery checkup', 'status': 'scheduled',
                'doctor_name': 'Dr. Brown', 'notes': '', 'created_at': datetime.now().isoformat()
            },
            {
                'id': 4, 'patient_id': 3, 'appointment_date': '2025-02-25', 'appointment_time': '11:15',
                'type': 'Imaging', 'reason': 'X-ray examination', 'status': 'scheduled',
                'doctor_name': 'Dr. Davis', 'notes': '', 'created_at': datetime.now().isoformat()
            },
            {
                'id': 5, 'patient_id': 4, 'appointment_date': '2025-03-05', 'appointment_time': '08:30',
                'type': 'Vaccination', 'reason': 'Annual flu shot', 'status': 'scheduled',
                'doctor_name': 'Dr. Wilson', 'notes': '', 'created_at': datetime.now().isoformat()
            }
        ]
        
        save_json_file(APPOINTMENTS_FILE, dummy_appointments)
        print(f"Inserted {len(dummy_appointments)} dummy appointment records")
    
    print("Database initialized successfully!")

def add_patient(lastname, firstname, middlename=None, suffix=None, birthday=None, address=None, 
                phone=None, email=None, emergency_contact_name=None, emergency_contact_phone=None,
                medical_history=None, allergies=None, blood_type=None):
    """Add a new patient to the database with enhanced fields"""
    try:
        patients = load_json_file(PATIENTS_FILE, [])
        
        # Create new patient record
        new_patient = {
            'id': get_next_id(patients),
            'lastname': lastname,
            'firstname': firstname,
            'middlename': middlename,
            'suffix': suffix,
            'birthday': birthday,
            'address': address,
            'phone': phone,
            'email': email,
            'emergency_contact_name': emergency_contact_name,
            'emergency_contact_phone': emergency_contact_phone,
            'medical_history': medical_history,
            'allergies': allergies,
            'blood_type': blood_type,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'is_new': 1,
            'status': 'active'
        }
        
        patients.append(new_patient)
        
        if save_json_file(PATIENTS_FILE, patients):
            print(f"Successfully added patient: {firstname} {lastname} (ID: {new_patient['id']})")
            return {'success': True, 'patient': new_patient, 'patient_id': new_patient['id']}
        else:
            return {'success': False, 'error': 'Failed to save patient data'}
        
    except Exception as e:
        print(f"Error adding patient: {str(e)}")
        return {'success': False, 'error': str(e)}

def import_patients_from_csv(file_path):
    """Import patients from a CSV file"""
    import csv
    
    try:
        patients = load_json_file(PATIENTS_FILE, [])
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
                    existing = any(
                        p['lastname'].lower() == patient_data['lastname'].lower() and
                        p['firstname'].lower() == patient_data['firstname'].lower() and
                        (p.get('middlename') or '').lower() == (patient_data['middlename'] or '').lower() and
                        p['birthday'] == patient_data['birthday']
                        for p in patients
                    )
                    
                    if existing:
                        errors.append(f"Row {row_num}: Patient already exists")
                        continue
                    
                    # Create new patient record
                    new_patient = {
                        'id': get_next_id(patients),
                        'lastname': patient_data['lastname'],
                        'firstname': patient_data['firstname'],
                        'middlename': patient_data['middlename'],
                        'suffix': patient_data['suffix'],
                        'birthday': patient_data['birthday'],
                        'address': patient_data['address'],
                        'phone': patient_data['phone'],
                        'email': patient_data['email'],
                        'emergency_contact_name': patient_data['emergency_contact_name'],
                        'emergency_contact_phone': patient_data['emergency_contact_phone'],
                        'medical_history': patient_data['medical_history'],
                        'allergies': patient_data['allergies'],
                        'blood_type': patient_data['blood_type'],
                        'created_at': datetime.now().isoformat(),
                        'updated_at': datetime.now().isoformat(),
                        'is_new': 0,
                        'status': 'active'
                    }
                    
                    patients.append(new_patient)
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")
        
        # Save updated patients data
        save_json_file(PATIENTS_FILE, patients)
        
        # Record the import
        imports = load_json_file(IMPORTS_FILE, [])
        import_record = {
            'id': get_next_id(imports),
            'filename': os.path.basename(file_path),
            'import_date': datetime.now().isoformat(),
            'records_imported': imported_count,
            'import_type': 'csv',
            'status': 'completed'
        }
        imports.append(import_record)
        save_json_file(IMPORTS_FILE, imports)
        
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
        patients = load_json_file(PATIENTS_FILE, [])
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
                    existing = any(
                        p['lastname'].lower() == patient['lastname'].lower() and
                        p['firstname'].lower() == patient['firstname'].lower() and
                        (p.get('middlename') or '').lower() == (patient.get('middlename') or '').lower() and
                        p['birthday'] == patient['birthday']
                        for p in patients
                    )
                    
                    if existing:
                        errors.append(f"Patient {index + 1}: Already exists")
                        continue
                    
                    # Create new patient record
                    new_patient = {
                        'id': get_next_id(patients),
                        'lastname': patient['lastname'],
                        'firstname': patient['firstname'],
                        'middlename': patient.get('middlename'),
                        'suffix': patient.get('suffix'),
                        'birthday': patient['birthday'],
                        'address': patient['address'],
                        'phone': patient.get('phone'),
                        'email': patient.get('email'),
                        'emergency_contact_name': patient.get('emergency_contact_name'),
                        'emergency_contact_phone': patient.get('emergency_contact_phone'),
                        'medical_history': patient.get('medical_history'),
                        'allergies': patient.get('allergies'),
                        'blood_type': patient.get('blood_type'),
                        'created_at': datetime.now().isoformat(),
                        'updated_at': datetime.now().isoformat(),
                        'is_new': 0,
                        'status': 'active'
                    }
                    
                    patients.append(new_patient)
                    imported_count += 1
                    
                except Exception as e:
                    errors.append(f"Patient {index + 1}: {str(e)}")
        
        # Save updated patients data
        save_json_file(PATIENTS_FILE, patients)
        
        # Record the import
        imports = load_json_file(IMPORTS_FILE, [])
        import_record = {
            'id': get_next_id(imports),
            'filename': os.path.basename(file_path),
            'import_date': datetime.now().isoformat(),
            'records_imported': imported_count,
            'import_type': 'json',
            'status': 'completed'
        }
        imports.append(import_record)
        save_json_file(IMPORTS_FILE, imports)
        
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
    patients = load_json_file(PATIENTS_FILE, [])
    
    # Filter active patients
    active_patients = [p for p in patients if p.get('status') == 'active']
    
    # Apply search filters
    results = []
    for patient in active_patients:
        match = True
        
        if lastname and patient.get('lastname', '').lower().strip() != lastname.lower().strip():
            match = False
        if firstname and patient.get('firstname', '').lower().strip() != firstname.lower().strip():
            match = False
        if middlename and (patient.get('middlename') or '').lower().strip() != middlename.lower().strip():
            match = False
        if suffix and (patient.get('suffix') or '').lower().strip() != suffix.lower().strip():
            match = False
        if birthday and patient.get('birthday', '').strip() != birthday.strip():
            match = False
        if address and address.lower().strip() not in patient.get('address', '').lower().strip():
            match = False
        
        if match:
            results.append(patient)
    
    return results

def get_all_patients():
    """Get all active patients from the database"""
    patients = load_json_file(PATIENTS_FILE, [])
    active_patients = [p for p in patients if p.get('status') == 'active']
    return sorted(active_patients, key=lambda x: (x.get('lastname', ''), x.get('firstname', '')))

def get_patient_by_id(patient_id):
    """Get a specific patient by ID"""
    try:
        patients = load_json_file(PATIENTS_FILE, [])
        for patient in patients:
            if patient.get('id') == patient_id and patient.get('status') == 'active':
                return patient
        return None
    except Exception as e:
        print(f"Error getting patient by ID: {str(e)}")
        return None

def get_import_history():
    """Get the history of data imports"""
    try:
        imports = load_json_file(IMPORTS_FILE, [])
        return sorted(imports, key=lambda x: x.get('import_date', ''), reverse=True)
    except Exception as e:
        print(f"Error getting import history: {str(e)}")
        return []

def get_appointments_by_patient_id(patient_id):
    """Get all appointments for a specific patient"""
    try:
        appointments = load_json_file(APPOINTMENTS_FILE, [])
        patient_appointments = [a for a in appointments if a.get('patient_id') == patient_id]
        return sorted(patient_appointments, key=lambda x: x.get('appointment_date', ''), reverse=True)
    except Exception as e:
        print(f"Error getting appointments: {str(e)}")
        return []

def create_appointment(patient_id, appointment_date, appointment_time='09:00', appointment_type='Consultation', 
                      reason='', doctor_name=''):
    """Create a new appointment for a patient"""
    try:
        appointments = load_json_file(APPOINTMENTS_FILE, [])
        
        new_appointment = {
            'id': get_next_id(appointments),
            'patient_id': patient_id,
            'appointment_date': appointment_date,
            'appointment_time': appointment_time,
            'type': appointment_type,
            'reason': reason,
            'status': 'scheduled',
            'doctor_name': doctor_name,
            'notes': '',
            'created_at': datetime.now().isoformat()
        }
        
        appointments.append(new_appointment)
        
        if save_json_file(APPOINTMENTS_FILE, appointments):
            return {'success': True, 'appointment_id': new_appointment['id']}
        else:
            return {'success': False, 'error': 'Failed to save appointment'}
        
    except Exception as e:
        print(f"Error creating appointment: {str(e)}")
        return {'success': False, 'error': str(e)}

def get_all_appointments():
    """Get all appointments with patient information"""
    try:
        appointments = load_json_file(APPOINTMENTS_FILE, [])
        patients = load_json_file(PATIENTS_FILE, [])
        
        # Create a patient lookup dictionary
        patient_lookup = {p['id']: p for p in patients if p.get('status') == 'active'}
        
        # Add patient names to appointments
        enriched_appointments = []
        for appointment in appointments:
            patient_id = appointment.get('patient_id')
            patient = patient_lookup.get(patient_id)
            
            if patient:
                appointment_copy = appointment.copy()
                patient_name_parts = [
                    patient.get('firstname', ''),
                    patient.get('middlename', ''),
                    patient.get('lastname', ''),
                    patient.get('suffix', '')
                ]
                appointment_copy['patient_name'] = ' '.join(filter(None, patient_name_parts))
                enriched_appointments.append(appointment_copy)
        
        return sorted(enriched_appointments, key=lambda x: x.get('appointment_date', ''), reverse=True)
        
    except Exception as e:
        print(f"Error getting all appointments: {str(e)}")
        return []

if __name__ == '__main__':
    # Initialize database when script is run directly
    init_database()
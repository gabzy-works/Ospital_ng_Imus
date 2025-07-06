from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import os
from database import (init_database, search_patients, get_all_patients, add_patient, 
                     get_patient_by_id, import_patients_from_csv, import_patients_from_json, 
                     get_import_history, get_appointments_by_patient_id, create_appointment,
                     get_all_appointments)
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'data/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database on startup
init_database()

# Form field data for the hospital form
FORM_FIELDS = [
    {"id": "lastname", "label": "Lastname", "placeholder": "Enter lastname"},
    {"id": "firstname", "label": "Firstname", "placeholder": "Enter firstname"},
    {"id": "middlename", "label": "Middlename", "placeholder": "Enter middlename"},
    {"id": "suffix", "label": "Suffix (Optional)", "placeholder": "Enter suffix (optional)"},
]

@app.route('/')
def index():
    """Main page route - displays the hospital search form"""
    return render_template('index.html', form_fields=FORM_FIELDS)

@app.route('/search', methods=['POST'])
def search_patient():
    """Handle patient search form submission"""
    # Get form data
    lastname = request.form.get('lastname', '').strip()
    firstname = request.form.get('firstname', '').strip()
    middlename = request.form.get('middlename', '').strip()
    suffix = request.form.get('suffix', '').strip()
    birthday = request.form.get('birthday', '').strip()
    
    # Debug: print received values
    print(f"Received search: lastname='{lastname}', firstname='{firstname}', middlename='{middlename}', suffix='{suffix}', birthday='{birthday}'")

    # Validate that at least lastname, firstname, and middlename are provided
    if not (lastname and firstname and middlename):
        return jsonify({
            'success': False,
            'message': 'Please provide lastname, firstname, and middlename for search.'
        }), 400

    try:
        # Debug: print parameters to be used for search
        print(f"Searching with: lastname={lastname}, firstname={firstname}, middlename={middlename}, suffix={suffix if suffix else None}, birthday={birthday if birthday else None}")
        
        # Search database for matching patients
        patients = search_patients(
            lastname=lastname,
            firstname=firstname,
            middlename=middlename,
            suffix=suffix if suffix else None,
            birthday=birthday if birthday else None
        )
        
        return jsonify({
            'success': True,
            'message': f'Found {len(patients)} patient(s)',
            'data': {
                'patients': patients,
                'search_criteria': {
                    'lastname': lastname,
                    'firstname': firstname,
                    'middlename': middlename,
                    'suffix': suffix,
                    'birthday': birthday
                },
                'search_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    except Exception as e:
        print(f"Database search error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Database error: {str(e)}'
        }), 500

@app.route('/patients')
def list_patients():
    """API endpoint to get all patients (for testing)"""
    try:
        patients = get_all_patients()
        return jsonify({
            'success': True,
            'data': patients,
            'count': len(patients)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Database error: {str(e)}'
        }), 500

@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected'
    })

@app.route('/add_patient', methods=['POST'])
def add_patient_route():
    """Add a new patient to the database with enhanced fields"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Extract and validate required fields
        lastname = data.get('lastname', '').strip()
        firstname = data.get('firstname', '').strip()
        middlename = data.get('middlename', '').strip()
        suffix = data.get('suffix', '').strip() or None
        birthday = data.get('birthday', '').strip()
        address = data.get('address', '').strip()
        
        # Optional fields
        phone = data.get('phone', '').strip() or None
        email = data.get('email', '').strip() or None
        emergency_contact_name = data.get('emergency_contact_name', '').strip() or None
        emergency_contact_phone = data.get('emergency_contact_phone', '').strip() or None
        medical_history = data.get('medical_history', '').strip() or None
        allergies = data.get('allergies', '').strip() or None
        blood_type = data.get('blood_type', '').strip() or None

        # Validate required fields
        if not (lastname and firstname and middlename and birthday and address):
            return jsonify({
                'success': False,
                'message': 'All required fields must be provided (lastname, firstname, middlename, birthday, address).'
            }), 400

        # Validate birthday format (should be YYYY-MM-DD)
        try:
            datetime.strptime(birthday, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Invalid birthday format. Please use YYYY-MM-DD format.'
            }), 400

        # Check if patient already exists
        existing_patients = search_patients(
            lastname=lastname,
            firstname=firstname,
            middlename=middlename,
            suffix=suffix,
            birthday=birthday
        )
        
        if existing_patients:
            return jsonify({
                'success': False,
                'message': f'Patient "{firstname} {lastname}" with the same details already exists in the database.'
            }), 409

        # Add patient to database
        result = add_patient(
            lastname=lastname,
            firstname=firstname,
            middlename=middlename,
            suffix=suffix,
            birthday=birthday,
            address=address,
            phone=phone,
            email=email,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_phone=emergency_contact_phone,
            medical_history=medical_history,
            allergies=allergies,
            blood_type=blood_type
        )
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': f'Patient "{firstname} {lastname}" has been successfully added to the database!',
                'patient_id': result['patient_id'],
                'patient': result['patient']
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': f'Failed to add patient: {result["error"]}'
            }), 500
            
    except Exception as e:
        print(f"Error in add_patient_route: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/import_patients', methods=['POST'])
def import_patients():
    """Import patients from uploaded CSV or JSON file"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No file uploaded'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            }), 400
        
        # Check file extension
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if file_ext not in ['csv', 'json']:
            return jsonify({
                'success': False,
                'message': 'Only CSV and JSON files are supported'
            }), 400
        
        # Save uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Import based on file type
        if file_ext == 'csv':
            result = import_patients_from_csv(file_path)
        else:  # json
            result = import_patients_from_json(file_path)
        
        # Clean up uploaded file
        try:
            os.remove(file_path)
        except:
            pass
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': f'Successfully imported {result["imported_count"]} patients',
                'imported_count': result['imported_count'],
                'errors': result['errors'],
                'total_errors': result['total_errors']
            })
        else:
            return jsonify({
                'success': False,
                'message': f'Import failed: {result["error"]}',
                'imported_count': result['imported_count'],
                'errors': result['errors']
            }), 500
            
    except Exception as e:
        print(f"Error in import_patients: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/import_history')
def import_history():
    """Get the history of data imports"""
    try:
        imports = get_import_history()
        return jsonify({
            'success': True,
            'imports': imports
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Database error: {str(e)}'
        }), 500

@app.route('/appointments/<int:patient_id>', methods=['GET'])
def get_appointments(patient_id):
    """Get all appointments for a patient"""
    try:
        # First check if patient exists
        patient = get_patient_by_id(patient_id)
        if not patient:
            return jsonify({
                "success": False, 
                "message": "Patient not found"
            }), 404
        
        # Get appointments for the patient
        appointments = get_appointments_by_patient_id(patient_id)
        
        return jsonify({
            "success": True, 
            "appointments": appointments,
            "patient": patient
        })
        
    except Exception as e:
        print(f"Error getting appointments: {str(e)}")
        return jsonify({
            "success": False, 
            "message": f"Database error: {str(e)}"
        }), 500

@app.route('/appointments', methods=['POST'])
def create_appointment_route():
    """Create a new appointment for a patient"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False, 
                "message": "No data provided"
            }), 400
        
        patient_id = data.get('patient_id')
        appointment_date = data.get('appointment_date')
        appointment_time = data.get('appointment_time', '09:00')
        appointment_type = data.get('type', 'Consultation')
        reason = data.get('reason', '')
        doctor_name = data.get('doctor_name', '')
        
        if not patient_id or not appointment_date:
            return jsonify({
                "success": False, 
                "message": "Missing patient_id or appointment_date"
            }), 400
        
        # Validate that patient exists
        patient = get_patient_by_id(patient_id)
        if not patient:
            return jsonify({
                "success": False, 
                "message": "Patient not found"
            }), 404
        
        # Validate date format
        try:
            datetime.strptime(appointment_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                "success": False, 
                "message": "Invalid date format. Please use YYYY-MM-DD format."
            }), 400
        
        result = create_appointment(
            patient_id=patient_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            appointment_type=appointment_type,
            reason=reason,
            doctor_name=doctor_name
        )
        
        if result['success']:
            return jsonify({
                "success": True, 
                "message": "Appointment created successfully",
                "appointment_id": result['appointment_id']
            }), 201
        else:
            return jsonify({
                "success": False, 
                "message": f"Failed to create appointment: {result['error']}"
            }), 500
        
    except Exception as e:
        print(f"Error creating appointment: {str(e)}")
        return jsonify({
            "success": False, 
            "message": f"Database error: {str(e)}"
        }), 500

@app.route('/admin/login', methods=['POST'])
def admin_login():
    """Handle admin login"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        # Simple hardcoded admin credentials (in production, use proper authentication)
        if username == 'admin' and password == 'admin123':
            return jsonify({
                'success': True,
                'message': 'Login successful'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid username or password'
            }), 401
            
    except Exception as e:
        print(f"Error in admin login: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/admin/appointments', methods=['GET'])
def get_all_appointments_route():
    """Get all appointments with patient information for admin dashboard"""
    try:
        appointments = get_all_appointments()
        
        return jsonify({
            "success": True, 
            "appointments": appointments,
            "count": len(appointments)
        })
        
    except Exception as e:
        print(f"Error getting all appointments: {str(e)}")
        return jsonify({
            "success": False, 
            "message": f"Database error: {str(e)}"
        }), 500

if __name__ == '__main__':
    # Create static and templates directories if they don't exist
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    os.makedirs('data/uploads', exist_ok=True)
    
    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)
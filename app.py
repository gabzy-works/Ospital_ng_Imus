from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
from database import init_database, search_patients, get_all_patients, add_patient, get_patient_by_id
import sqlite3

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'

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
    """Add a new patient to the database"""
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
        suffix = data.get('suffix', '').strip() or None  # Convert empty string to None
        birthday = data.get('birthday', '').strip()
        address = data.get('address', '').strip()

        # Validate required fields
        if not (lastname and firstname and middlename and birthday and address):
            return jsonify({
                'success': False,
                'message': 'All fields except suffix are required (lastname, firstname, middlename, birthday, address).'
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
            address=address
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

@app.route('/appointments/<int:patient_id>', methods=['GET'])
def get_appointments(patient_id):
    """Get all appointments for a patient"""
    try:
        conn = sqlite3.connect('data/patients.db')
        cursor = conn.cursor()
        
        # First check if patient exists
        patient = get_patient_by_id(patient_id)
        if not patient:
            return jsonify({
                "success": False, 
                "message": "Patient not found"
            }), 404
        
        # Get appointments for the patient
        cursor.execute(
            "SELECT * FROM appointments WHERE patient_id = ? ORDER BY appointment_date DESC", 
            (patient_id,)
        )
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        appointments = [dict(zip(columns, row)) for row in results]
        conn.close()
        
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
def create_appointment():
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
        reason = data.get('reason', '')
        
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
        
        conn = sqlite3.connect('data/patients.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO appointments (patient_id, appointment_date, reason) VALUES (?, ?, ?)",
            (patient_id, appointment_date, reason)
        )
        conn.commit()
        appointment_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            "success": True, 
            "message": "Appointment created successfully",
            "appointment_id": appointment_id
        }), 201
        
    except Exception as e:
        print(f"Error creating appointment: {str(e)}")
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
    
    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)
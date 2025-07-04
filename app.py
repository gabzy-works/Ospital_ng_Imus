from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
from database import init_database, search_patients, get_all_patients
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
    birthday = request.form.get('birthday', '').strip()
    # Debug: print received values
    print(f"Received search: lastname='{lastname}', firstname='{firstname}', middlename='{middlename}', birthday='{birthday}'")

    # Validate that at least lastname, firstname, and middlename are provided
    if not (lastname and firstname and middlename):
        return jsonify({
            'success': False,
            'message': 'Please provide lastname, firstname, and middlename for search.'
        }), 400

    try:
        # Debug: print parameters to be used for search
        print(f"Searching with: lastname={lastname}, firstname={firstname}, middlename={middlename}, birthday={birthday if birthday else None}")
        # Search database for matching patients (birthday is optional)
        patients = search_patients(
            lastname=lastname,
            firstname=firstname,
            middlename=middlename,
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
                    'birthday': birthday
                },
                'search_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    except Exception as e:
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
def add_patient():
    data = request.get_json()
    lastname = data.get('lastname', '').strip()
    firstname = data.get('firstname', '').strip()
    middlename = data.get('middlename', '').strip()
    suffix = data.get('suffix', '').strip()
    birthday = data.get('birthday', '').strip()
    address = data.get('address', '').strip()

    if not (lastname and firstname and middlename and birthday and address):
        return {'success': False, 'message': 'All fields except suffix are required.'}, 400

    try:
        conn = sqlite3.connect('data/patients.db')
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO patients (lastname, firstname, middlename, suffix, birthday, address)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (lastname, firstname, middlename, suffix, birthday, address)
        )
        conn.commit()
        conn.close()
        return {'success': True, 'message': 'Patient added successfully!'}
    except Exception as e:
        return {'success': False, 'message': f'Failed to add patient: {str(e)}'}, 500

@app.route('/appointments/<int:patient_id>', methods=['GET'])
def get_appointments(patient_id):
    """Get all appointments for a patient"""
    conn = sqlite3.connect('data/patients.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments WHERE patient_id = ? ORDER BY appointment_date DESC", (patient_id,))
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    appointments = [dict(zip(columns, row)) for row in results]
    conn.close()
    return jsonify({"success": True, "appointments": appointments})

@app.route('/appointments', methods=['POST'])
def create_appointment():
    """Create a new appointment for a patient"""
    data = request.get_json()
    patient_id = data.get('patient_id')
    appointment_date = data.get('appointment_date')
    reason = data.get('reason', '')
    if not patient_id or not appointment_date:
        return jsonify({"success": False, "message": "Missing patient_id or appointment_date"}), 400
    conn = sqlite3.connect('data/patients.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO appointments (patient_id, appointment_date, reason) VALUES (?, ?, ?)",
        (patient_id, appointment_date, reason)
    )
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Appointment created"})

if __name__ == '__main__':
    # Create static and templates directories if they don't exist
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)
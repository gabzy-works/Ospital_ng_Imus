from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
from database import init_database, search_patients, get_all_patients

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
    {"id": "suffix", "label": "Suffix (If Applicable)", "placeholder": "Enter suffix (if applicable)"},
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
    
    # Basic validation - at least one field must be provided
    if not any([lastname, firstname, middlename, suffix, birthday]):
        return jsonify({
            'success': False,
            'message': 'Please provide at least one search criteria'
        }), 400
    
    try:
        # Search database for matching patients
        patients = search_patients(
            lastname=lastname if lastname else None,
            firstname=firstname if firstname else None,
            middlename=middlename if middlename else None,
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

if __name__ == '__main__':
    # Create static and templates directories if they don't exist
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)
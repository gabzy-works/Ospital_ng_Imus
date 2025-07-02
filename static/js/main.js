// Main JavaScript functionality for the hospital search form

document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const resultsModal = document.getElementById('resultsModal');
    const closeButton = document.querySelector('.close-button');
    const resultsContent = document.getElementById('resultsContent');

    // Handle form submission
    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Show loading overlay
        loadingOverlay.classList.remove('hidden');
        
        // Get form data
        const formData = new FormData(searchForm);
        
        // Ensure birthday is in YYYY-MM-DD format only if provided
        const birthdayInput = searchForm.querySelector('#birthday');
        if (birthdayInput && birthdayInput.value) {
            const date = new Date(birthdayInput.value);
            if (!isNaN(date.getTime())) {
                const yyyy = date.getFullYear();
                const mm = String(date.getMonth() + 1).padStart(2, '0');
                const dd = String(date.getDate()).padStart(2, '0');
                const formatted = `${yyyy}-${mm}-${dd}`;
                formData.set('birthday', formatted);
            }
        }
        
        // Send AJAX request to Flask backend
        fetch('/search', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading overlay
            loadingOverlay.classList.add('hidden');
            
            if (data.success) {
                // Display results in modal
                displayResults(data.data);
                resultsModal.classList.remove('hidden');
            } else {
                // Show error message
                alert('Error: ' + data.message);
            }
        })
        .catch(error => {
            // Hide loading overlay
            loadingOverlay.classList.add('hidden');
            console.error('Error:', error);
            alert('An error occurred while searching. Please try again.');
        });
    });

    // Close modal functionality
    closeButton.addEventListener('click', function() {
        resultsModal.classList.add('hidden');
    });

    // Close modal when clicking outside
    resultsModal.addEventListener('click', function(e) {
        if (e.target === resultsModal) {
            resultsModal.classList.add('hidden');
        }
    });

    // Function to display search results
    function displayResults(data) {
        let html = '<div class="search-results">';
        
        if (data.patients && data.patients.length > 0) {
            html += '<h3>Patient Search Results (' + data.patients.length + ' found)</h3>';
            
            data.patients.forEach(function(patient, index) {
                html += '<div class="result-item">';
                html += '<h4>Patient #' + (index + 1) + '</h4>';
                html += '<div class="patient-info-flex">';
                html += '<div class="patient-photo-col">';
                html += '<img src="/Patient ID sample.png" alt="Patient ID" class="patient-photo" />';
                html += '</div>';
                html += '<div class="patient-details-col">';
                html += '<p><strong>Last Name:</strong> ' + (patient.lastname || 'N/A') + '</p>';
                html += '<p><strong>First Name:</strong> ' + (patient.firstname || 'N/A') + '</p>';
                html += '<p><strong>Middle Name:</strong> ' + (patient.middlename || 'N/A') + '</p>';
                html += '<p><strong>Suffix:</strong> ' + (patient.suffix || 'N/A') + '</p>';
                html += '<p><strong>Birthday:</strong> ' + (patient.birthday || 'N/A') + '</p>';
                html += '<p><strong>Patient ID:</strong> ' + (patient.id || 'N/A') + '</p>';
                html += '<p><strong>Address:</strong> ' + (patient.address || 'N/A') + '</p>';
                html += '</div>';
                html += '</div>';
                html += '</div>';
            });
        } else {
            html += '<h3>No Patients Found</h3>';
            html += '<div class="result-item">';
            html += '<p>No patients match your search criteria. Please try different search terms.</p>';
            html += '</div>';
        }
        
        html += '<div class="search-info">';
        html += '<h4>Search Criteria Used:</h4>';
        html += '<p><strong>Last Name:</strong> ' + (data.search_criteria.lastname || 'Not specified') + '</p>';
        html += '<p><strong>First Name:</strong> ' + (data.search_criteria.firstname || 'Not specified') + '</p>';
        html += '<p><strong>Middle Name:</strong> ' + (data.search_criteria.middlename || 'Not specified') + '</p>';
        html += '<p><strong>Suffix:</strong> ' + (data.search_criteria.suffix || 'Not specified') + '</p>';
        html += '<p><strong>Birthday:</strong> ' + (data.search_criteria.birthday || 'Not specified') + '</p>';
        html += '<p><strong>Search Time:</strong> ' + data.search_time + '</p>';
        html += '</div>';
        html += '</div>';
        
        resultsContent.innerHTML = html;
    }

    // Add some interactive effects to form inputs
    const formInputs = document.querySelectorAll('.form-input');
    formInputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0px 6px 8px rgba(0, 0, 0, 0.3)';
        });
        
        input.addEventListener('blur', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0px 4px 4px rgba(0, 0, 0, 0.25)';
        });
    });
});

// Add some CSS for the results display
const style = document.createElement('style');
style.textContent = `
    .search-results {
        font-family: 'Inter', sans-serif;
        max-height: 70vh;
        overflow-y: auto;
    }
    
    .search-results h3 {
        color: #05196a;
        margin-bottom: 20px;
        font-size: 24px;
        font-weight: 800;
        text-align: center;
    }
    
    .result-item {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 4px solid #05196a;
    }
    
    .result-item h4 {
        color: #05196a;
        margin-bottom: 15px;
        font-size: 18px;
        font-weight: 700;
    }
    
    /* FLEX LAYOUT for patient info */
    .patient-info-flex {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 24px;
    }
    .patient-photo-col {
        flex: 0 0 auto;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .patient-photo {
        width: 80px;
        height: 100px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.10);
        background: #fff;
        border: 2px solid #e0e0e0;
    }
    .patient-details-col {
        flex: 1 1 0%;
        display: flex;
        flex-direction: column;
        gap: 0;
    }
    .patient-details-col p {
        margin-bottom: 0;
        font-size: 14px;
        line-height: 1.4;
    }
    .patient-details-col strong {
        color: #05196a;
        font-weight: 600;
    }
    
    .search-info {
        background-color: #e9ecef;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
    }
    
    .search-info h4 {
        color: #05196a;
        margin-bottom: 10px;
        font-size: 16px;
    }
    
    .search-info p {
        font-size: 12px;
        margin-bottom: 5px;
        color: #666;
    }
    
    .modal-content {
        max-width: 800px;
        width: 95%;
    }
`;
document.head.appendChild(style);
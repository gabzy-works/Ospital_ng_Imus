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
        html += '<h3>Patient Search Results</h3>';
        html += '<div class="result-item">';
        html += '<p><strong>Last Name:</strong> ' + (data.lastname || 'N/A') + '</p>';
        html += '<p><strong>First Name:</strong> ' + (data.firstname || 'N/A') + '</p>';
        html += '<p><strong>Middle Name:</strong> ' + (data.middlename || 'N/A') + '</p>';
        html += '<p><strong>Suffix:</strong> ' + (data.suffix || 'N/A') + '</p>';
        html += '<p><strong>Birthday:</strong> ' + (data.birthday || 'N/A') + '</p>';
        html += '<p><strong>Search Time:</strong> ' + data.search_time + '</p>';
        html += '</div>';
        html += '<p class="note"><em>Note: This is a demo. In a real application, this would search the patient database.</em></p>';
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
    }
    
    .search-results h3 {
        color: #05196a;
        margin-bottom: 20px;
        font-size: 24px;
        font-weight: 800;
    }
    
    .result-item {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    
    .result-item p {
        margin-bottom: 8px;
        font-size: 16px;
    }
    
    .result-item strong {
        color: #05196a;
        font-weight: 600;
    }
    
    .note {
        font-style: italic;
        color: #666;
        text-align: center;
        margin-top: 20px;
    }
`;
document.head.appendChild(style);
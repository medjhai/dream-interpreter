/**
 * Dream Interpreter - Client-side JavaScript
 * Handles the form submission and display of dream interpretations
 */

// Get DOM elements
const dreamInput = document.getElementById('dream-input');
const interpretBtn = document.getElementById('interpret-btn');
const resultContainer = document.getElementById('result-container');
const resultElement = document.getElementById('result');
const loadingElement = document.getElementById('loading');
const errorContainer = document.getElementById('error-container');
const errorMessage = document.getElementById('error-message');

/**
 * Send the dream text to the server for interpretation
 */
function sendDream() {
    // Get dream text from textarea
    const dreamText = dreamInput.value.trim();
    
    // Validate input
    if (!dreamText) {
        showError('Per favore, inserisci il testo del tuo sogno.');
        return;
    }
    
    // Hide any previous error
    hideError();
    
    // Show loading indicator
    showLoading();
    
    // Make the request to the server
    fetch('/interpret', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ dream: dreamText })
    })
    .then(response => {
        // Check if response is ok
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Si è verificato un errore durante l\'interpretazione.');
            });
        }
        return response.json();
    })
    .then(data => {
        // Display the interpretation
        hideLoading();
        displayInterpretation(data.interpretation);
    })
    .catch(error => {
        // Handle errors
        hideLoading();
        showError(error.message || 'Si è verificato un errore durante la comunicazione con il server.');
        console.error('Error:', error);
    });
}

/**
 * Display the dream interpretation
 * @param {string} interpretation - The dream interpretation text
 */
function displayInterpretation(interpretation) {
    resultElement.innerHTML = interpretation;
    resultContainer.classList.remove('d-none');
    // Smooth scroll to the result
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Show loading indicator
 */
function showLoading() {
    loadingElement.classList.remove('d-none');
    resultElement.classList.add('d-none');
    resultContainer.classList.remove('d-none');
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    loadingElement.classList.add('d-none');
    resultElement.classList.remove('d-none');
}

/**
 * Show error message
 * @param {string} message - The error message to display
 */
function showError(message) {
    errorMessage.textContent = message;
    errorContainer.classList.remove('d-none');
    // Smooth scroll to the error
    errorContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Hide error message
 */
function hideError() {
    errorContainer.classList.add('d-none');
}

// Add event listener for Enter key in textarea
dreamInput.addEventListener('keydown', function(event) {
    // Check if Enter key was pressed while holding Ctrl or Command
    if ((event.key === 'Enter' && (event.ctrlKey || event.metaKey))) {
        sendDream();
    }
});

// Add event listener for button click
interpretBtn.addEventListener('click', sendDream);

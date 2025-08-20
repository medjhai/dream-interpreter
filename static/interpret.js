// DOM elements
const dreamInput = document.getElementById('dream-input');
const dreamTitle = document.getElementById('dream-title');
const interpretBtn = document.getElementById('interpret-btn');
const resultContainer = document.getElementById('result-container');
const resultElement = document.getElementById('result');
const loadingElement = document.getElementById('loading');
const errorContainer = document.getElementById('error-container');
const errorMessage = document.getElementById('error-message');
const resultActions = document.getElementById('result-actions');

/**
 * Send the dream text and preferences to the server for interpretation
 */
function sendDream() {
    // Get dream text from textarea
    const dreamText = dreamInput.value.trim();
    const title = dreamTitle.value.trim();
    
    // Get selected mood from radio buttons
    let mood = "";
    const moodRadios = document.querySelectorAll('input[name="mood"]:checked');
    if (moodRadios.length > 0) {
        mood = moodRadios[0].value;
    }
    
    // Get selected style
    const styleSelect = document.getElementById('style-select');
    const style = styleSelect.value;
    
    // Validate input
    if (!dreamText) {
        showError('Per favore, inserisci il testo del tuo sogno.');
        return;
    }
    
    // Hide any previous error
    hideError();
    
    // Show loading indicator
    showLoading();
    
    // Make the request to the server with additional parameters
    fetch('/interpret', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
            dream: dreamText,
            title: title,
            mood: mood,
            style: style
        })
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
        showResultActions();
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
    const btnText = interpretBtn.querySelector('.btn-text');
    const btnLoading = interpretBtn.querySelector('.btn-loading');
    
    btnText.classList.add('d-none');
    btnLoading.classList.remove('d-none');
    interpretBtn.disabled = true;
    
    loadingElement.classList.remove('d-none');
    resultElement.classList.add('d-none');
    resultContainer.classList.remove('d-none');
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    const btnText = interpretBtn.querySelector('.btn-text');
    const btnLoading = interpretBtn.querySelector('.btn-loading');
    
    btnText.classList.remove('d-none');
    btnLoading.classList.add('d-none');
    interpretBtn.disabled = false;
    
    loadingElement.classList.add('d-none');
    resultElement.classList.remove('d-none');
}

/**
 * Show result actions
 */
function showResultActions() {
    resultActions.classList.remove('d-none');
}

/**
 * Hide result actions
 */
function hideResultActions() {
    resultActions.classList.add('d-none');
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

/**
 * Reset the form for a new dream interpretation
 */
function resetForm() {
    dreamInput.value = '';
    dreamTitle.value = '';
    
    // Reset mood selection to neutral
    document.getElementById('mood-none').checked = true;
    
    // Reset style to neutral
    document.getElementById('style-select').value = 'neutro';
    
    // Hide result container and actions
    resultContainer.classList.add('d-none');
    hideResultActions();
    hideError();
    
    // Focus on dream input
    dreamInput.focus();
    
    // Scroll to top of form
    document.querySelector('.dream-card').scrollIntoView({ behavior: 'smooth', block: 'start' });
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

// Focus on dream input when page loads
document.addEventListener('DOMContentLoaded', function() {
    dreamInput.focus();
});
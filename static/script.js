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

let currentDreamId = null;
let selectedRating = 0;

/**
 * Send the dream text and preferences to the server for interpretation
 */
function sendDream() {
    // Get dream text from textarea
    const dreamText = dreamInput.value.trim();
    
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
        currentDreamId = data.dreamId;
        displayInterpretation(data.interpretation);
        displayFeedbackForm();
        updateSentimentIndicator(data.sentimentScore);
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

/**
 * Display feedback form
 */
function displayFeedbackForm() {
    const feedbackHtml = `
        <div id="feedback-section" class="mt-4">
            <h4>Come valuti questa interpretazione?</h4>
            <div class="rating">
                ${Array.from({length: 5}, (_, i) => i + 1)
                    .map(num => `
                        <span class="star" data-rating="${num}">★</span>
                    `).join('')}
            </div>
            <textarea id="feedback-comment" 
                      class="form-control mt-3" 
                      placeholder="Commenti aggiuntivi (opzionale)"></textarea>
            <button onclick="submitFeedback()" 
                    class="btn btn-primary mt-3">
                Invia Feedback
            </button>
        </div>`;
    
    resultElement.insertAdjacentHTML('beforeend', feedbackHtml);
    
    // Add event listeners to stars
    document.querySelectorAll('.star').forEach(star => {
        star.addEventListener('mouseover', function() {
            const rating = this.dataset.rating;
            highlightStars(rating);
        });
        
        star.addEventListener('click', function() {
            const rating = this.dataset.rating;
            selectStars(rating);
        });
    });
    
    // Reset stars on mouse out
    document.querySelector('.rating').addEventListener('mouseout', function() {
        resetStars();
    });
}

/**
 * Highlight stars on hover
 * @param {number} rating - The rating to highlight
 */
function highlightStars(rating) {
    document.querySelectorAll('.star').forEach(star => {
        star.classList.toggle('hover', star.dataset.rating <= rating);
    });
}

/**
 * Select stars on click
 * @param {number} rating - The rating to select
 */
function selectStars(rating) {
    document.querySelectorAll('.star').forEach(star => {
        star.classList.toggle('selected', star.dataset.rating <= rating);
    });
    selectedRating = rating;
}

/**
 * Reset stars on mouse out
 */
function resetStars() {
    document.querySelectorAll('.star').forEach(star => {
        star.classList.remove('hover');
    });
}

/**
 * Submit feedback
 */
function submitFeedback() {
    if (!selectedRating) {
        showError('Per favore seleziona un rating prima di inviare il feedback');
        return;
    }
    
    const comment = document.getElementById('feedback-comment').value;
    
    fetch('/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            dreamId: currentDreamId,
            rating: selectedRating,
            comment: comment
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        document.getElementById('feedback-section').innerHTML = 
            '<div class="alert alert-success">Grazie per il tuo feedback!</div>';
        loadStats();
    })
    .catch(error => {
        showError(error.message || 'Errore nell\'invio del feedback');
    });
}

/**
 * Update sentiment indicator
 * @param {number} score - The sentiment score
 */
function updateSentimentIndicator(score) {
    let sentiment, color;
    if (score > 0.3) {
        sentiment = 'Positivo';
        color = 'success';
    } else if (score < -0.3) {
        sentiment = 'Negativo';
        color = 'danger';
    } else {
        sentiment = 'Neutro';
        color = 'info';
    }
    
    const sentimentHtml = `
        <div class="sentiment-indicator mt-3">
            <span class="badge bg-${color}">
                Tono emotivo: ${sentiment}
            </span>
        </div>`;
    
    resultElement.insertAdjacentHTML('afterbegin', sentimentHtml);
}

/**
 * Load statistics
 */
function loadStats() {
    fetch('/stats')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            displayStats(data);
        })
        .catch(error => {
            console.error('Error loading stats:', error);
        });
}

/**
 * Display statistics
 * @param {object} stats - The statistics data
 */
function displayStats(stats) {
    const statsHtml = `
        <div class="stats-section mt-4">
            <h4>Statistiche Interpretazioni</h4>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">${stats.totalDreams}</div>
                    <div class="stat-label">Sogni Interpretati</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${stats.averageRating}/5</div>
                    <div class="stat-label">Rating Medio</div>
                </div>
                <div class="stat-item">
                    <div class="sentiment-distribution">
                        <div class="positive" style="width: ${stats.sentimentDistribution.positive}%"></div>
                        <div class="neutral" style="width: ${stats.sentimentDistribution.neutral}%"></div>
                        <div class="negative" style="width: ${stats.sentimentDistribution.negative}%"></div>
                    </div>
                    <div class="stat-label">Distribuzione Sentiment</div>
                </div>
            </div>
        </div>`;
    
    const statsContainer = document.getElementById('stats-container') || 
                          document.createElement('div');
    statsContainer.id = 'stats-container';
    statsContainer.innerHTML = statsHtml;
    
    if (!document.getElementById('stats-container')) {
        document.querySelector('.dream-app-container').appendChild(statsContainer);
    }
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

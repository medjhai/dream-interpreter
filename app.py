import os
from flask import Flask, render_template, request, jsonify
from dream_interpreter import interpret_dream
import logging
from functools import wraps
from datetime import datetime, timedelta
from collections import defaultdict
import re
from sqlalchemy import func
from models import Dream, Feedback, get_session, init_db

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Initialize database
init_db()

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rate limiting configuration
RATE_LIMIT = 20  # requests
RATE_LIMIT_PERIOD = 60  # seconds
request_counts = defaultdict(list)

def validate_dream_text(text):
    """Validate dream text input"""
    if not text or len(text.strip()) < 10:
        raise ValueError("Il testo del sogno deve essere almeno 10 caratteri")
    if len(text) > 5000:
        raise ValueError("Il testo del sogno non può superare i 5000 caratteri")
    # Check for basic content filtering
    if re.search(r'(hate|violence|explicit)', text.lower()):
        raise ValueError("Il contenuto non è appropriato")
    return text.strip()

def validate_style(style):
    """Validate interpretation style"""
    valid_styles = ["neutro", "poetico", "scientifico", "spirituale", "consolatorio"]
    if style not in valid_styles:
        raise ValueError(f"Stile non valido. Scegli tra: {', '.join(valid_styles)}")
    return style

def validate_mood(mood):
    """Validate mood input"""
    if mood and len(mood) > 50:
        raise ValueError("La descrizione dell'umore è troppo lunga")
    return mood.strip()

def rate_limit(f):
    """Rate limiting decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        now = datetime.now()
        ip = request.remote_addr
        
        # Clean old requests
        request_counts[ip] = [t for t in request_counts[ip] 
                            if t > now - timedelta(seconds=RATE_LIMIT_PERIOD)]
        
        if len(request_counts[ip]) >= RATE_LIMIT:
            logger.warning(f"Rate limit exceeded for IP: {ip}")
            return jsonify({
                'error': 'Hai superato il limite di richieste. Riprova tra qualche minuto.'
            }), 429
            
        request_counts[ip].append(now)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Render the main page of the dream interpreter app."""
    return render_template('index.html')

@app.route('/interpret', methods=['POST'])
@rate_limit
def interpret():
    """Process the dream interpretation request with enhanced validation and rate limiting."""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Dati non validi'}), 400

        # Validate dream text
        try:
            dream_text = validate_dream_text(data.get('dream', ''))
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

        # Validate optional parameters
        try:
            mood = validate_mood(data.get('mood', ''))
            style = validate_style(data.get('style', 'neutro'))
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

        # Create new dream entry
        session = get_session()
        dream = Dream(
            text=dream_text,
            mood=mood,
            style=style
        )
        
        # Analyze sentiment
        dream.analyze_sentiment()
        
        # Get interpretation
        interpretation = interpret_dream(dream_text, mood=mood, style=style)
        dream.interpretation = interpretation
        
        # Save to database
        session.add(dream)
        session.commit()
        
        # Log successful interpretation
        logger.info(f"Successfully interpreted dream ID: {dream.id}")
        
        return jsonify({
            'interpretation': interpretation,
            'dreamId': dream.id,
            'sentimentScore': dream.sentiment_score
        })
    
    except Exception as e:
        logger.error(f"Error interpreting dream: {str(e)}")
        return jsonify({
            'error': 'Si è verificato un errore durante l\'interpretazione del sogno'
        }), 500

@app.route('/feedback', methods=['POST'])
@rate_limit
def submit_feedback():
    """Submit feedback for a dream interpretation"""
    try:
        data = request.json
        if not data or 'dreamId' not in data or 'rating' not in data:
            return jsonify({'error': 'Dati feedback non validi'}), 400
            
        dream_id = data['dreamId']
        rating = int(data['rating'])
        comment = data.get('comment', '')
        
        # Validate rating
        if not 1 <= rating <= 5:
            return jsonify({'error': 'Il rating deve essere tra 1 e 5'}), 400
            
        session = get_session()
        dream = session.query(Dream).get(dream_id)
        
        if not dream:
            return jsonify({'error': 'Sogno non trovato'}), 404
            
        feedback = Feedback(
            dream_id=dream_id,
            rating=rating,
            comment=comment
        )
        
        session.add(feedback)
        session.commit()
        
        logger.info(f"Feedback submitted for dream ID: {dream_id}")
        
        return jsonify({'message': 'Feedback ricevuto con successo'})
        
    except Exception as e:
        logger.error(f"Error submitting feedback: {str(e)}")
        return jsonify({
            'error': 'Si è verificato un errore durante l\'invio del feedback'
        }), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get statistics about dream interpretations"""
    try:
        session = get_session()
        total_dreams = session.query(Dream).count()
        avg_rating = session.query(func.avg(Feedback.rating)).scalar() or 0
        sentiment_distribution = {
            'positive': session.query(Dream).filter(Dream.sentiment_score > 0.3).count(),
            'neutral': session.query(Dream).filter(
                Dream.sentiment_score.between(-0.3, 0.3)
            ).count(),
            'negative': session.query(Dream).filter(Dream.sentiment_score < -0.3).count()
        }
        
        return jsonify({
            'totalDreams': total_dreams,
            'averageRating': round(float(avg_rating), 2),
            'sentimentDistribution': sentiment_distribution
        })
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({
            'error': 'Si è verificato un errore nel recupero delle statistiche'
        }), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        'error': 'Hai superato il limite di richieste. Riprova tra qualche minuto.'
    }), 429

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({
        'error': 'Si è verificato un errore interno. Riprova più tardi.'
    }), 500

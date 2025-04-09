import os
from flask import Flask, render_template, request, jsonify
from dream_interpreter import interpret_dream

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

@app.route('/')
def index():
    """Render the main page of the dream interpreter app."""
    return render_template('index.html')

@app.route('/interpret', methods=['POST'])
def interpret():
    """
    Process the dream interpretation request.
    
    Expects JSON with:
    - 'dream' key containing the dream text
    - 'mood' key containing the emotional state (optional)
    - 'style' key containing the interpretation style (optional)
    
    Returns JSON with 'interpretation' key containing the interpretation.
    """
    try:
        data = request.json
        if not data or 'dream' not in data:
            return jsonify({'error': 'No dream text provided'}), 400
        
        dream_text = data.get('dream', '').strip()
        if not dream_text:
            return jsonify({'error': 'Dream text cannot be empty'}), 400
        
        # Get optional mood and style parameters
        mood = data.get('mood', '')
        style = data.get('style', 'neutro')
        
        # Pass all parameters to the interpreter
        interpretation = interpret_dream(dream_text, mood=mood, style=style)
        return jsonify({'interpretation': interpretation})
    
    except Exception as e:
        app.logger.error(f"Error interpreting dream: {str(e)}")
        return jsonify({'error': 'An error occurred while interpreting your dream'}), 500

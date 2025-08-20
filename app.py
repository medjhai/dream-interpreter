import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.middleware.proxy_fix import ProxyFix
from models import db, User, Dream
from dream_interpreter import interpret_dream

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    'pool_pre_ping': True,
    "pool_recycle": 300,
}

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Effettua il login per accedere a questa pagina.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create tables
with app.app_context():
    db.create_all()
    logging.info("Database tables created")

# Add custom Jinja filters
@app.template_filter('nl2br')
def nl2br_filter(text):
    """Convert newlines to HTML line breaks"""
    import re
    return re.sub(r'\n', '<br>', str(text))

@app.template_filter('date_diff_days')
def date_diff_days(date):
    """Calculate days between date and now"""
    from datetime import datetime
    diff = datetime.now() - date
    return diff.days

@app.route('/')
def index():
    """Main page - shows login or dashboard based on authentication status."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': 'Username e password sono richiesti'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            return jsonify({'success': True, 'redirect': url_for('dashboard')})
        else:
            return jsonify({'error': 'Credenziali non valide'}), 401
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page and user creation."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not all([username, email, password]):
            return jsonify({'error': 'Tutti i campi sono richiesti'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'La password deve essere di almeno 6 caratteri'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username già in uso'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email già registrata'}), 400
        
        # Create new user
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return jsonify({'success': True, 'redirect': url_for('dashboard')})
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error creating user: {str(e)}")
            return jsonify({'error': 'Errore durante la registrazione'}), 500
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with dream history."""
    recent_dreams = Dream.query.filter_by(user_id=current_user.id).order_by(Dream.created_at.desc()).limit(5).all()
    return render_template('dashboard.html', user=current_user, recent_dreams=recent_dreams)

@app.route('/interpret', methods=['GET', 'POST'])
@login_required
def interpret():
    """Dream interpretation page and processing."""
    if request.method == 'GET':
        return render_template('interpret.html')
    
    try:
        data = request.get_json()
        if not data or 'dream' not in data:
            return jsonify({'error': 'Testo del sogno mancante'}), 400
        
        dream_text = data.get('dream', '').strip()
        if not dream_text:
            return jsonify({'error': 'Il testo del sogno non può essere vuoto'}), 400
        
        # Get optional parameters
        mood = data.get('mood', '')
        style = data.get('style', 'neutro')
        title = data.get('title', '').strip()
        
        # Generate interpretation
        interpretation = interpret_dream(dream_text, mood=mood, style=style)
        
        # Save dream to database
        dream = Dream()
        dream.title = title or f"Sogno del {datetime.now().strftime('%d/%m/%Y')}"
        dream.content = dream_text
        dream.mood = mood
        dream.interpretation_style = style
        dream.interpretation = interpretation
        dream.user_id = current_user.id
        
        db.session.add(dream)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'interpretation': interpretation,
            'dream_id': dream.id
        })
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error interpreting dream: {str(e)}")
        return jsonify({'error': 'Errore durante l\'interpretazione del sogno'}), 500

@app.route('/dreams')
@login_required
def dreams_history():
    """Show user's dream history."""
    page = request.args.get('page', 1, type=int)
    dreams = Dream.query.filter_by(user_id=current_user.id).order_by(Dream.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    return render_template('dreams.html', dreams=dreams)

@app.route('/dream/<int:dream_id>')
@login_required
def view_dream(dream_id):
    """View a specific dream and its interpretation."""
    dream = Dream.query.filter_by(id=dream_id, user_id=current_user.id).first_or_404()
    return render_template('dream_detail.html', dream=dream)

@app.route('/dream/<int:dream_id>/delete', methods=['POST'])
@login_required
def delete_dream(dream_id):
    """Delete a dream."""
    dream = Dream.query.filter_by(id=dream_id, user_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(dream)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error deleting dream: {str(e)}")
        return jsonify({'error': 'Errore durante l\'eliminazione'}), 500

@app.route('/logout')
@login_required
def logout():
    """Logout user."""
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    """User profile page."""
    dream_count = Dream.query.filter_by(user_id=current_user.id).count()
    return render_template('profile.html', user=current_user, dream_count=dream_count)

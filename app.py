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
    "pool_timeout": 20,
    "pool_size": 5,
    "max_overflow": 10,
}

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # type: ignore
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

@app.template_filter('days_since')
def days_since(date):
    """Calculate days since date"""
    from datetime import datetime
    if not date:
        return 0
    diff = datetime.now() - date
    return diff.days

@app.route('/')
def index():
    """Main page - shows login or dashboard based on authentication status."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return render_template('landing_minimal.html')

@app.route('/home')
@login_required
def home():
    """Dreamy home page with floating circles."""
    return render_template('home_minimal.html')

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
    
    return render_template('login_minimal.html')

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
    
    return render_template('register_minimal.html')

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with dream history."""
    recent_dreams = Dream.query.filter_by(user_id=current_user.id).order_by(Dream.created_at.desc()).limit(5).all()
    dream_count = Dream.query.filter_by(user_id=current_user.id).count()
    
    # Calculate streak days
    from datetime import timedelta
    dream_dates = sorted(set([d.created_at.date() for d in Dream.query.filter_by(user_id=current_user.id).all()]), reverse=True)
    streak_days = 0
    if dream_dates:
        current_date = datetime.now().date()
        for i, dream_date in enumerate(dream_dates):
            if dream_date == current_date - timedelta(days=i):
                streak_days += 1
            else:
                break
    
    # Get favorite mood
    moods = [d.mood for d in Dream.query.filter_by(user_id=current_user.id).all() if d.mood]
    favorite_mood = None
    if moods:
        from collections import Counter
        mood_counter = Counter(moods)
        common_mood = mood_counter.most_common(1)[0][0]
        mood_emojis = {'felice': '😊', 'triste': '😢', 'ansioso': '😰', 'rabbioso': '😠', 'confuso': '😕'}
        favorite_mood = mood_emojis.get(common_mood, '😐')
    
    return render_template('dashboard_minimal.html', 
                         user=current_user, 
                         recent_dreams=recent_dreams,
                         dream_count=dream_count,
                         streak_days=streak_days,
                         favorite_mood=favorite_mood)

@app.route('/interpret', methods=['GET', 'POST'])
@login_required
def interpret():
    """Dream interpretation page and processing."""
    if request.method == 'GET':
        return render_template('interpret_minimal.html')
    
    try:
        data = request.get_json()
        if not data or 'content' not in data:
            return jsonify({'error': 'Testo del sogno mancante'}), 400
        
        dream_text = data.get('content', '').strip()
        if not dream_text:
            return jsonify({'error': 'Il testo del sogno non può essere vuoto'}), 400
        
        # Get optional parameters
        mood = data.get('mood', '')
        style = data.get('interpretation_style', 'neutro')
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
    return render_template('dreams_minimal.html', dreams=dreams)

@app.route('/dream/<int:dream_id>')
@login_required
def view_dream(dream_id):
    """View a specific dream and its interpretation."""
    dream = Dream.query.filter_by(id=dream_id, user_id=current_user.id).first_or_404()
    return render_template('dream_detail_minimal.html', dream=dream)

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
    """User profile page with mood calendar data."""
    dream_count = Dream.query.filter_by(user_id=current_user.id).count()
    
    # Get dreams with dates and moods for calendar
    dreams_with_moods = Dream.query.filter_by(user_id=current_user.id)\
                                  .filter(Dream.mood.isnot(None))\
                                  .order_by(Dream.created_at.desc())\
                                  .all()
    
    # Create mood data dictionary for JavaScript
    mood_data = {}
    for dream in dreams_with_moods:
        date_key = dream.created_at.strftime('%Y-%m-%d')
        if date_key not in mood_data:
            mood_data[date_key] = []
        mood_data[date_key].append({
            'mood': dream.mood,
            'title': dream.title,
            'id': dream.id
        })
    
    return render_template('profile_minimal.html', 
                         user=current_user, 
                         dream_count=dream_count,
                         mood_data=mood_data)

@app.route('/settings', methods=['GET', 'POST'])
@login_required 
def settings():
    """User settings page."""
    if request.method == 'POST':
        # Handle settings updates via AJAX
        try:
            data = request.get_json()
            setting_type = data.get('type')
            value = data.get('value')
            
            # In future: save user preferences to database
            # For now, just return success
            return jsonify({'success': True, 'message': f'Impostazione {setting_type} aggiornata'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('settings_minimal.html')

@app.route('/search')
@login_required
def search_dreams():
    """Search dreams with advanced filters."""
    query = request.args.get('q', '').strip()
    mood = request.args.get('mood', '').strip()
    style = request.args.get('style', '').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()
    export = request.args.get('export', '').strip()
    
    # Base query for user's dreams
    dreams_query = Dream.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if query:
        dreams_query = dreams_query.filter(
            (Dream.title.ilike(f'%{query}%')) | 
            (Dream.content.ilike(f'%{query}%')) |
            (Dream.interpretation.ilike(f'%{query}%'))
        )
    
    if mood:
        dreams_query = dreams_query.filter(Dream.mood == mood)
    
    if style:
        dreams_query = dreams_query.filter(Dream.interpretation_style == style)
    
    if date_from:
        try:
            from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
            dreams_query = dreams_query.filter(Dream.created_at >= from_date)
        except ValueError:
            pass
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
            dreams_query = dreams_query.filter(Dream.created_at <= to_date)
        except ValueError:
            pass
    
    dreams = dreams_query.order_by(Dream.created_at.desc()).all()
    
    # Handle CSV export
    if export == 'csv':
        import csv
        from io import StringIO
        from flask import Response
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Titolo', 'Data', 'Mood', 'Stile', 'Contenuto', 'Interpretazione'])
        
        for dream in dreams:
            writer.writerow([
                dream.title,
                dream.created_at.strftime('%Y-%m-%d'),
                dream.mood or '',
                dream.interpretation_style or '',
                dream.content,
                dream.interpretation or ''
            ])
        
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=sogni_export.csv'}
        )
    
    # Get popular keywords from user's dreams
    popular_keywords = []
    if current_user.id:
        # Simple keyword extraction from dream content
        import re
        from collections import Counter
        
        all_content = ' '.join([d.content for d in Dream.query.filter_by(user_id=current_user.id).all()])
        words = re.findall(r'\b\w{4,}\b', all_content.lower())
        common_words = ['sono', 'stata', 'stato', 'molto', 'anche', 'della', 'nella', 'come', 'quando', 'dove']
        filtered_words = [w for w in words if w not in common_words]
        
        word_counts = Counter(filtered_words).most_common(10)
        popular_keywords = [{'word': word, 'count': count} for word, count in word_counts]
    
    return render_template('search_minimal.html', 
                         dreams=dreams, 
                         popular_keywords=popular_keywords)

@app.route('/stats')
@login_required 
def stats():
    """Statistics and analytics page."""
    from datetime import datetime, timedelta
    from collections import Counter
    import json
    
    user_dreams = Dream.query.filter_by(user_id=current_user.id).all()
    total_dreams = len(user_dreams)
    
    if not user_dreams:
        # Empty state for new users
        return render_template('stats_minimal.html', 
                             total_dreams=0,
                             dreams_this_month=0,
                             most_common_mood=None,
                             dream_frequency=0,
                             current_streak=0,
                             mood_distribution=[],
                             common_themes=[],
                             style_preferences=[],
                             dream_activity_data='{"labels": [], "data": []}',
                             mood_chart_data='{"labels": [], "data": [], "colors": []}',
                             calendar_data='{}')
    
    # Calculate basic stats
    now = datetime.now()
    this_month_start = now.replace(day=1)
    dreams_this_month = len([d for d in user_dreams if d.created_at >= this_month_start])
    
    # Most common mood
    moods = [d.mood for d in user_dreams if d.mood]
    most_common_mood = None
    if moods:
        mood_counter = Counter(moods)
        common_mood_name = mood_counter.most_common(1)[0][0]
        mood_emojis = {
            'felice': '😊',
            'triste': '😢', 
            'ansioso': '😰',
            'rabbioso': '😠',
            'confuso': '😕'
        }
        most_common_mood = {
            'name': common_mood_name.title(),
            'emoji': mood_emojis.get(common_mood_name, '😐')
        }
    
    # Dream frequency (dreams per week in last 30 days)
    thirty_days_ago = now - timedelta(days=30)
    recent_dreams = [d for d in user_dreams if d.created_at >= thirty_days_ago]
    dream_frequency = round(len(recent_dreams) / 4.3, 1) if recent_dreams else 0
    
    # Current streak (consecutive days with dreams)
    current_streak = 0
    dream_dates = sorted(set([d.created_at.date() for d in user_dreams]), reverse=True)
    if dream_dates:
        current_date = now.date()
        for i, dream_date in enumerate(dream_dates):
            if dream_date == current_date - timedelta(days=i):
                current_streak += 1
            else:
                break
    
    # Mood distribution for chart
    mood_colors = {
        'felice': '#00b894',
        'triste': '#0984e3', 
        'ansioso': '#fdcb6e',
        'rabbioso': '#e17055',
        'confuso': '#a29bfe'
    }
    
    mood_emojis = {
        'felice': '😊',
        'triste': '😢',
        'ansioso': '😰', 
        'rabbioso': '😠',
        'confuso': '😕'
    }
    
    mood_distribution = []
    if moods:
        mood_counts = Counter(moods)
        for mood, count in mood_counts.items():
            mood_distribution.append({
                'name': mood.title(),
                'emoji': mood_emojis.get(mood, '😐'),
                'count': count,
                'color': mood_colors.get(mood, '#6c5ce7')
            })
    
    # Common themes (keywords)
    import re
    from collections import Counter
    
    all_content = ' '.join([d.content for d in user_dreams])
    words = re.findall(r'\b\w{4,}\b', all_content.lower())
    common_words = ['sono', 'stata', 'stato', 'molto', 'anche', 'della', 'nella', 'come', 'quando', 'dove', 'casa', 'persone', 'tempo']
    filtered_words = [w for w in words if w not in common_words]
    
    word_counts = Counter(filtered_words).most_common(8)
    common_themes = [{'word': word.title(), 'count': count} for word, count in word_counts]
    
    # Style preferences
    styles = [d.interpretation_style for d in user_dreams if d.interpretation_style]
    style_counts = Counter(styles)
    style_preferences = [{'name': style, 'count': count} for style, count in style_counts.items()]
    
    # Chart data for frontend
    last_30_days = [(now - timedelta(days=i)).date() for i in range(29, -1, -1)]
    daily_counts = []
    for date in last_30_days:
        count = len([d for d in user_dreams if d.created_at.date() == date])
        daily_counts.append(count)
    
    dream_activity_data = json.dumps({
        'labels': [d.strftime('%d/%m') for d in last_30_days],
        'data': daily_counts
    })
    
    mood_chart_data = json.dumps({
        'labels': [m['name'] for m in mood_distribution],
        'data': [m['count'] for m in mood_distribution], 
        'colors': [m['color'] for m in mood_distribution]
    })
    
    return render_template('stats_minimal.html',
                         total_dreams=total_dreams,
                         dreams_this_month=dreams_this_month,
                         most_common_mood=most_common_mood,
                         dream_frequency=dream_frequency,
                         current_streak=current_streak,
                         mood_distribution=mood_distribution,
                         common_themes=common_themes,
                         style_preferences=style_preferences,
                         dream_activity_data=dream_activity_data,
                         mood_chart_data=mood_chart_data,
                         calendar_data='{}')

@app.route('/api/dream-activity')
@login_required
def api_dream_activity():
    """API endpoint for dream activity data."""
    from datetime import datetime, timedelta
    import json
    
    period = int(request.args.get('period', 30))
    now = datetime.now()
    
    # Get dreams from the specified period
    start_date = now - timedelta(days=period-1)
    user_dreams = Dream.query.filter_by(user_id=current_user.id).filter(
        Dream.created_at >= start_date
    ).all()
    
    # Create daily counts
    date_range = [(now - timedelta(days=i)).date() for i in range(period-1, -1, -1)]
    daily_counts = []
    for date in date_range:
        count = len([d for d in user_dreams if d.created_at.date() == date])
        daily_counts.append(count)
    
    return jsonify({
        'labels': [d.strftime('%d/%m') for d in date_range],
        'data': daily_counts
    })

@app.route('/export-data')
@login_required
def export_data():
    """Export all user data as JSON."""
    import json
    from flask import Response
    
    dreams = Dream.query.filter_by(user_id=current_user.id).all()
    
    export_data = {
        'user': {
            'username': current_user.username,
            'email': current_user.email,
            'created_at': current_user.created_at.isoformat() if current_user.created_at else None
        },
        'dreams': []
    }
    
    for dream in dreams:
        export_data['dreams'].append({
            'id': dream.id,
            'title': dream.title,
            'content': dream.content,
            'mood': dream.mood,
            'interpretation_style': dream.interpretation_style,
            'interpretation': dream.interpretation,
            'created_at': dream.created_at.isoformat()
        })
    
    response_data = json.dumps(export_data, indent=2, ensure_ascii=False)
    
    return Response(
        response_data,
        mimetype='application/json',
        headers={
            'Content-Disposition': 'attachment; filename=sogni_completi_export.json'
        }
    )

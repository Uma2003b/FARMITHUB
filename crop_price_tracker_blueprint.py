from flask import Blueprint, render_template, request, jsonify, redirect, current_app
import requests
import re
from functools import wraps
import os

crop_price_tracker_bp = Blueprint('crop_price_tracker', __name__,
                                 template_folder=os.path.join('Crop_Prices_Tracker', 'templates'),
                                 static_folder=os.path.join('Crop_Prices_Tracker', 'static'))

# Global API config
API_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
API_PARAMS = {
    "api-key": "579b464db66ec23bdd000001c43ef34767ce496343897dfb1893102b",
    "format": "json",
    "limit": 2000
}

# Input validation helper functions
def sanitize_input(text, max_length=255):
    """Sanitize text input"""
    if not isinstance(text, str):
        return ""
    # Remove any potentially dangerous characters
    cleaned = re.sub(r'[<>"\']', '', text.strip())
    return cleaned[:max_length]

def validate_required_fields(required_fields):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            for field in required_fields:
                if field not in request.form or not request.form[field].strip():
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Load data once (to avoid repeated API hits)
def load_data():
    try:
        response = requests.get(API_URL, params=API_PARAMS, timeout=10)
        response.raise_for_status()
        return response.json().get("records", [])
    except requests.RequestException as e:
        print(f"API request failed: {str(e)}")  # Use print instead of logger at module level
        return []

DATA = load_data()
print(f"Loaded {len(DATA)} records from external API for crop price tracker.")

@crop_price_tracker_bp.route('/')
def home():
    return redirect('/crop_price_tracker/crop_price_tracker')

@crop_price_tracker_bp.route('/crop_price_tracker', methods=['GET', 'POST'])
def crop_price_tracker():
    try:
        crops = sorted({record['commodity'] for record in DATA if record.get('commodity')})
        result = []
        error = None

        if request.method == 'POST':
            # Sanitize inputs
            crop = sanitize_input(request.form.get('crop', ''), 100)
            state = sanitize_input(request.form.get('state', ''), 100)
            market = sanitize_input(request.form.get('market', ''), 100)

            # Validate inputs
            if not crop or not state or not market:
                error = "All fields (crop, state, market) are required."
            else:
                result = [
                    r for r in DATA
                    if r.get('commodity', '').lower() == crop.lower()
                    and r.get('state', '').lower() == state.lower()
                    and r.get('market', '').lower() == market.lower()
                ]

                if not result:
                    error = "No data found for the given crop, state, and market."

        return render_template('crop_price_tracker.html', crops=crops, result=result, error=error)
        
    except Exception as e:
        current_app.logger.error(f"Crop price tracker error: {str(e)}")
        return render_template('crop_price_tracker.html', crops=[], result=[], error="An error occurred while processing your request.")

@crop_price_tracker_bp.route('/get_states')
def get_states():
    try:
        crop = sanitize_input(request.args.get('crop', ''), 100).lower()
        if not crop:
            return jsonify([])
            
        states = sorted({r['state'] for r in DATA if r.get('commodity', '').lower() == crop})
        return jsonify(states)
        
    except Exception as e:
        current_app.logger.error(f"Get states error: {str(e)}")
        return jsonify([])

@crop_price_tracker_bp.route('/get_markets')
def get_markets():
    try:
        crop = sanitize_input(request.args.get('crop', ''), 100).lower()
        state = sanitize_input(request.args.get('state', ''), 100).lower()
        
        if not crop or not state:
            return jsonify([])
            
        markets = sorted({
            r['market'] for r in DATA
            if r.get('commodity', '').lower() == crop and r.get('state', '').lower() == state
        })
        return jsonify(markets)
        
    except Exception as e:
        current_app.logger.error(f"Get markets error: {str(e)}")
        return jsonify([])
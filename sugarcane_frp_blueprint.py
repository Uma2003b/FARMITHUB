from flask import Blueprint, render_template, request, jsonify, redirect, current_app
import requests
import re
from functools import wraps
import os

sugarcane_frp_bp = Blueprint('sugarcane_frp', __name__,
                             template_folder=os.path.join('Sugarcane_FRP', 'templates'),
                             static_folder=os.path.join('Sugarcane_FRP', 'static'))

# Global API config
API_URL = "https://api.data.gov.in/resource/6546457d-a621-4a61-b114-8b3ad0888142"
API_PARAMS = {
    "api-key": "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b",
    "format": "json",
    "limit": 10
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
print(f"Loaded {len(DATA)} records from Sugarcane FRP API.")

@sugarcane_frp_bp.route('/')
def home():
    return redirect('/sugarcane_frp/sugarcane_frp')

@sugarcane_frp_bp.route('/sugarcane_frp', methods=['GET', 'POST'])
def sugarcane_frp():
    try:
        seasons = sorted({record['sugar_season'] for record in DATA if record.get('sugar_season')})
        result = DATA  # Default to all data
        error = None

        if request.method == 'POST':
            # Sanitize inputs
            season = sanitize_input(request.form.get('season', ''), 20)

            if season:
                result = [
                    r for r in DATA
                    if r.get('sugar_season', '') == season
                ]
                if not result:
                    error = "No data found for the selected season."
            else:
                result = DATA  # Show all if no filter

        # Sort result by sugar_season
        result = sorted(result, key=lambda x: x.get('sugar_season', ''))

        return render_template('sugarcane_frp.html', seasons=seasons, result=result, error=error)

    except Exception as e:
        current_app.logger.error(f"Sugarcane FRP error: {str(e)}")
        return render_template('sugarcane_frp.html', seasons=[], result=[], error="An error occurred while processing your request.")

@sugarcane_frp_bp.route('/get_seasons')
def get_seasons():
    try:
        seasons = sorted({r['sugar_season'] for r in DATA if r.get('sugar_season')})
        return jsonify(seasons)

    except Exception as e:
        current_app.logger.error(f"Get seasons error: {str(e)}")
        return jsonify([])

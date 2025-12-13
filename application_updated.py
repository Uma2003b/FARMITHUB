from flask import Flask, render_template, send_from_directory, jsonify, request, abort, Blueprint
import requests
import os

class MultiTemplateFinder(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.jinja_loader.searchpath.extend([
            os.path.join(self.root_path, 'Crop Recommendation', 'templates'),
            os.path.join(self.root_path, 'Crop_Planning', 'templates'),
            os.path.join(self.root_path, 'Crop_Prices_Tracker', 'templates'),
            os.path.join(self.root_path, 'Crop_Yield_Prediction', 'crop_yield_app', 'templates'),
            os.path.join(self.root_path, 'Labour_Alerts', 'templates'),
            os.path.join(self.root_path, 'Forum'),
            os.path.join(self.root_path, 'Sugarcane_FRP', 'templates'),
            os.path.join(self.root_path, 'District_Procurement', 'templates'),
        ])

application = MultiTemplateFinder(__name__, static_folder='static', template_folder='templates')

# Create Blueprint for crop recommendation
crop_recommendation_bp = Blueprint('crop_recommendation', __name__)

# Crop Price Tracker Data
API_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
API_PARAMS = {"api-key": "579b464db66ec23bdd000001c43ef34767ce496343897dfb1893102b", "format": "json", "limit": 2000}

def load_crop_data():
    try:
        response = requests.get(API_URL, params=API_PARAMS, timeout=10)
        response.raise_for_status()
        return response.json().get("records", [])
    except:
        return []

CROP_DATA = load_crop_data()

# Load ML Models
try:
    import joblib
    import numpy as np
    import pandas as pd
    
    # Crop Recommendation Models
    crop_model = joblib.load(os.path.join('Crop Recommendation', 'model', 'rf_model.pkl'))
    crop_label_encoder = joblib.load(os.path.join('Crop Recommendation', 'model', 'label_encoder.pkl'))
    print("Crop recommendation model loaded successfully")
    
    # Crop Yield Prediction Models (using PythonAnywhere files)
    crop_yield_model = joblib.load(os.path.join('Crop_Yield_Prediction', 'xgb_crop_model.pkl'))
    crop_encoder = joblib.load(os.path.join('Crop_Yield_Prediction', 'item_encoder.pkl'))
    season_encoder = joblib.load(os.path.join('Crop_Yield_Prediction', 'Season_encoder.pkl'))
    state_encoder = joblib.load(os.path.join('Crop_Yield_Prediction', 'State_encoder.pkl'))
    area_encoder = joblib.load(os.path.join('Crop_Yield_Prediction', 'area_encoder.pkl'))
    print("Crop yield prediction models loaded successfully")
    
except Exception as e:
    crop_model = None
    crop_label_encoder = None
    crop_yield_model = None
    crop_encoder = None
    area_encoder = None
    season_encoder = None
    state_encoder = None
    print(f"Could not load ML models: {e}")

@application.route('/')
def home():
    return render_template('index.html')

@application.route('/index.html')
def index_html():
    return render_template('index.html')


@application.route('/about')
def about():
    return render_template('about.html')

@application.route('/about.html')
def about_html():
    return render_template('about.html')

@application.route('/login')
def login():
    return render_template('login.html')

@application.route('/login.html')
def login_html():
    return render_template('login.html')

@application.route('/register')
def register():
    return render_template('register.html')

@application.route('/register.html')
def register_html():
    return render_template('register.html')

@application.route('/main')
def main():
    return render_template('main.html')

@application.route('/main.html')
def main_html():
    return render_template('main.html')

@application.route('/index_telugu.html')
def index_telugu():
    return render_template('index_telugu.html')

@application.route('/login_telugu.html')
def login_telugu():
    return render_template('login_telugu.html')

@application.route('/register_telugu.html')
def register_telugu():
    return render_template('register_telugu.html')

@application.route('/main_telugu.html')
def main_telugu():
    return render_template('main_telugu.html')

@application.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    # Accept any credentials and always succeed
    return jsonify({'success': True, 'message': 'Login successful', 'user': {'email': email, 'fullname': 'User', 'role': 'user'}})

@application.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    fullname = data.get('fullname')
    # Accept any credentials and always succeed
    return jsonify({'success': True, 'message': 'Registration successful', 'user': {'email': email, 'fullname': fullname or 'User', 'role': role or 'user'}})

@application.route('/<path:filename>')
def serve_static(filename):
    allowed_ext = ['css', 'js', 'png', 'jpg', 'jpeg', 'gif', 'svg', 'avif', 'webp', 'ico', 'woff', 'woff2', 'ttf', 'eot']
    if '.' in filename and filename.split('.')[-1].lower() in allowed_ext:
        try:
            return send_from_directory('.', filename)
        except:
            pass
    abort(404)

@application.route('/disease.html')
def disease():
    return render_template('disease.html')

@application.route('/disease_telugu.html')
def disease_telugu():
    return render_template('disease_telugu.html')

@application.route('/weather.html')
def weather():
    return render_template('weather.html')

@application.route('/weather_telugu.html')
def weather_telugu():
    return render_template('weather_telugu.html')

@application.route('/farmer.html')
def farmer():
    return render_template('farmer.html')

@application.route('/farmer_telugu.html')
def farmer_telugu():
    return render_template('farmer_telugu.html')

@application.route('/organic.html')
def organic():
    return render_template('organic.html')

@application.route('/organic_telugu.html')
def organic_telugu():
    return render_template('organic_telugu.html')

@application.route('/shopkeeper.html')
def shopkeeper():
    return render_template('shopkeeper.html')

@application.route('/shopkeeper_telugu.html')
def shopkeeper_telugu():
    return render_template('shopkeeper_telugu.html')

@application.route('/chat.html')
def chat():
    return render_template('chat.html')

@application.route('/chat_telugu.html')
def chat_telugu():
    return render_template('chat_telugu.html')

@application.route('/plantation.html')
def plantation():
    return render_template('plantation.html')

@application.route('/plantation_telugu.html')
def plantation_telugu():
    return render_template('plantation_telugu.html')

@application.route('/Crop_Planning/templates/cropplan.html')
@application.route('/crop_planning/')
def cropplan():
    return render_template('cropplan.html')

@application.route('/Labour_Alerts/templates/labour.html')
@application.route('/labour_alerts/')
def labour():
    return render_template('labour.html')

@application.route('/Labour_Alerts/templates/labour_telugu.html')
def labour_telugu():
    return render_template('labour_telugu.html')

@application.route('/Forum/forum.html')
@application.route('/forum_loan/')
def forum():
    return render_template('forum.html')

@application.route('/Forum/forum_telugu.html')
def forum_telugu():
    return render_template('forum_telugu.html')

@crop_recommendation_bp.route('/')
def index():
    return render_template('crop_recommendation.html')

@crop_recommendation_bp.route('/')
def home():
    return render_template('crop_recommendation.html')

@crop_recommendation_bp.route('/predict', methods=['POST'])
def predict():
    if not crop_model or not crop_label_encoder:
        # Fallback crop recommendation
        try:
            N = float(request.form['N'])
            P = float(request.form['P'])
            K = float(request.form['K'])
            temperature = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            ph = float(request.form['ph'])
            rainfall = float(request.form['rainfall'])
            
            # Simple rule-based recommendation
            if rainfall > 1000 and temperature > 25:
                crop = 'Rice'
            elif ph > 7 and K > 40:
                crop = 'Wheat'
            elif temperature > 30 and rainfall < 800:
                crop = 'Cotton'
            else:
                crop = 'Maize'
            
            params = {
                'N': N, 'P': P, 'K': K,
                'temperature': temperature,
                'humidity': humidity,
                'ph': ph,
                'rainfall': rainfall,
                'soil_type': None
            }
            
            return render_template('result.html', crop=crop, params=params, error=None)
        except Exception as e:
            return render_template('result.html', crop=None, params=None, error=str(e))

    try:
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        prediction = crop_model.predict(input_data)
        crop = crop_label_encoder.inverse_transform(prediction)[0]

        params = {
            'N': N, 'P': P, 'K': K,
            'temperature': temperature,
            'humidity': humidity,
            'ph': ph,
            'rainfall': rainfall,
            'soil_type': None
        }

        return render_template('result.html', crop=crop, params=params, error=None)
    except Exception as e:
        return render_template('result.html', crop=None, params=None, error=str(e))

@crop_recommendation_bp.route('/download_report', methods=['POST'])
def download_report():
    return jsonify({'error': 'PDF download not available'}), 503

application.register_blueprint(crop_recommendation_bp, url_prefix='/crop_recommendation')

crop_yield_bp = Blueprint('crop_yield', __name__)

@crop_yield_bp.route('/')
def index():
    # Complete dropdown options from dataset (always use full lists)
    crops = ['Arecanut', 'Arhar/Tur', 'Bajra', 'Banana', 'Barley', 'Black pepper', 'Cardamom', 'Cashewnut', 'Castor seed', 'Coconut', 'Coriander', 'Cotton(lint)', 'Dry chillies', 'Garlic', 'Ginger', 'Gram', 'Groundnut', 'Horse-gram', 'Jowar', 'Jute', 'Khesari', 'Linseed', 'Maize', 'Masoor', 'Mesta', 'Moong(Green Gram)', 'Niger seed', 'Onion', 'Other Cereals', 'Other Kharif pulses', 'Other Rabi pulses', 'Peas & beans (Pulses)', 'Potato', 'Ragi', 'Rapeseed &Mustard', 'Rice', 'Safflower', 'Sannhamp', 'Sesamum', 'Small millets', 'Soyabean', 'Sugarcane', 'Sunflower', 'Sweet potato', 'Tapioca', 'Tobacco', 'Turmeric', 'Urad', 'Wheat', 'other oilseeds']
    
    seasons = ['Autumn', 'Kharif', 'Rabi', 'Summer', 'Whole Year', 'Winter']
    
    states = ['Andhra Pradesh', 'Assam', 'Goa', 'Karnataka', 'Kerala', 'Meghalaya', 'Puducherry', 'Tamil Nadu', 'West Bengal']
    return render_template('index_fixed.html', crops=crops, seasons=seasons, states=states)

@crop_yield_bp.route('/predict', methods=['POST'])
def predict():
    if not crop_yield_model or not crop_encoder or not season_encoder or not state_encoder:
        try:
            if request.is_json:
                data = request.get_json()
                crop = data.get('crop')
                season = data.get('season')
                state = data.get('state')
                area = float(data.get('area', 0))
                production = float(data.get('production', 0))
            else:
                crop = request.form.get('crop')
                season = request.form.get('season')
                state = request.form.get('state')
                area = float(request.form.get('area', 0))
                production = float(request.form.get('production', 0))
            
            # Simple yield calculation (production/area)
            predicted_yield = round(production / area if area > 0 else 0, 2)
            
            params = {
                'crop': crop,
                'season': season,
                'state': state,
                'area': area,
                'production': production,
                'rainfall': 0,
                'year': 2024
            }
            
            if request.is_json:
                return jsonify({'success': True, 'predicted_yield': predicted_yield})
            else:
                return render_template('yield_result.html', prediction=predicted_yield, params=params, error=None)
        except Exception as e:
            if request.is_json:
                return jsonify({'error': str(e)}), 500
            else:
                return render_template('yield_result.html', error=str(e))
    
    try:
        # Handle both form data and JSON
        if request.is_json:
            data = request.get_json()
            crop = data.get('crop')
            season = data.get('season')
            state = data.get('state')
            area = float(data.get('area', 0))
            production = float(data.get('production', 0))
        else:
            crop = request.form.get('crop')
            season = request.form.get('season')
            state = request.form.get('state')
            area = float(request.form.get('area', 0))
            production = float(request.form.get('production', 0))
        
        # Encode categorical variables
        crop_encoded = crop_encoder.transform([crop])[0]
        season_encoded = season_encoder.transform([season])[0]
        state_encoded = state_encoder.transform([state])[0]
        
        # Create input array
        input_data = [[crop_encoded, season_encoded, state_encoded, area, production]]
        
        # Make prediction
        prediction = crop_yield_model.predict(input_data)[0]
        
        predicted_yield = round(prediction, 2)
        params = {
            'crop': crop,
            'season': season,
            'state': state,
            'area': area,
            'production': production,
            'rainfall': request.form.get('rainfall', 0) if not request.is_json else data.get('rainfall', 0),
            'year': request.form.get('year', 2024) if not request.is_json else data.get('year', 2024)
        }
        
        if request.is_json:
            return jsonify({'success': True, 'predicted_yield': predicted_yield})
        else:
            return render_template('yield_result.html', prediction=predicted_yield, params=params, error=None)
            
    except Exception as e:
        if request.is_json:
            return jsonify({'error': str(e)}), 500
        else:
            return render_template('yield_result.html', error=str(e))

# Add API endpoints for crop yield dropdowns
@crop_yield_bp.route('/api/crops')
def get_crops():
    crops = ['Arecanut', 'Arhar/Tur', 'Bajra', 'Banana', 'Barley', 'Black pepper', 'Cardamom', 'Cashewnut', 'Castor seed', 'Coconut', 'Coriander', 'Cotton(lint)', 'Dry chillies', 'Garlic', 'Ginger', 'Gram', 'Groundnut', 'Horse-gram', 'Jowar', 'Jute', 'Khesari', 'Linseed', 'Maize', 'Masoor', 'Mesta', 'Moong(Green Gram)', 'Niger seed', 'Onion', 'Other Cereals', 'Other Kharif pulses', 'Other Rabi pulses', 'Peas & beans (Pulses)', 'Potato', 'Ragi', 'Rapeseed &Mustard', 'Rice', 'Safflower', 'Sannhamp', 'Sesamum', 'Small millets', 'Soyabean', 'Sugarcane', 'Sunflower', 'Sweet potato', 'Tapioca', 'Tobacco', 'Turmeric', 'Urad', 'Wheat', 'other oilseeds']
    return jsonify(crops)

@crop_yield_bp.route('/api/seasons')
def get_seasons():
    seasons = ['Autumn', 'Kharif', 'Rabi', 'Summer', 'Whole Year', 'Winter']
    return jsonify(seasons)

@crop_yield_bp.route('/api/states')
def get_states():
    states = ['Andhra Pradesh', 'Assam', 'Goa', 'Karnataka', 'Kerala', 'Meghalaya', 'Puducherry', 'Tamil Nadu', 'West Bengal']
    return jsonify(states)

application.register_blueprint(crop_yield_bp, url_prefix='/crop_yield')

# Sugarcane FRP Blueprint
sugarcane_frp_bp = Blueprint('sugarcane_frp', __name__,
                             static_folder=os.path.join('Sugarcane_FRP', 'static'),
                             static_url_path='/static')

SUGARCANE_API_URL = "https://api.data.gov.in/resource/6546457d-a621-4a61-b114-8b3ad0888142"
SUGARCANE_API_PARAMS = {"api-key": "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b", "format": "json", "limit": 10}

def load_sugarcane_data():
    try:
        response = requests.get(SUGARCANE_API_URL, params=SUGARCANE_API_PARAMS, timeout=10)
        response.raise_for_status()
        return response.json().get("records", [])
    except:
        return []

SUGARCANE_DATA = load_sugarcane_data()

@sugarcane_frp_bp.route('/')
@sugarcane_frp_bp.route('/sugarcane_frp', methods=['GET', 'POST'])
def index():
    seasons = sorted({record['sugar_season'] for record in SUGARCANE_DATA if record.get('sugar_season')})
    result = SUGARCANE_DATA
    error = None

    if request.method == 'POST':
        season = request.form.get('season', '').strip()
        if season:
            result = [r for r in SUGARCANE_DATA if r.get('sugar_season', '') == season]
            if not result:
                error = "No data found for the selected season."

    result = sorted(result, key=lambda x: x.get('sugar_season', ''))
    return render_template('sugarcane_frp.html', seasons=seasons, result=result, error=error)

application.register_blueprint(sugarcane_frp_bp, url_prefix='/sugarcane_frp')

# District Procurement Blueprint
district_procurement_bp = Blueprint('district_procurement', __name__,
                                   static_folder=os.path.join('District_Procurement', 'static'),
                                   static_url_path='/static')

DISTRICT_API_URL = "https://api.data.gov.in/resource/3938e80b-28ce-42d8-b9e8-b8fa0a802172"
DISTRICT_API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"

@district_procurement_bp.route('/')
def index():
    season = request.args.get('season', '')
    district = request.args.get('district', '')
    commodity = request.args.get('commodity', '')

    params = {'api-key': DISTRICT_API_KEY, 'format': 'json', 'limit': 1000}
    if season:
        params['filters[season]'] = season
    if district:
        params['filters[district]'] = district
    if commodity:
        params['filters[commodity]'] = commodity

    try:
        response = requests.get(DISTRICT_API_URL, params=params, timeout=10)
        data = response.json()
        records = data.get('records', [])
    except:
        records = []

    seasons = sorted(set(record.get('season', '') for record in records if record.get('season')))
    districts = sorted(set(record.get('district', '') for record in records if record.get('district')))
    commodities = sorted(set(record.get('commodity', '') for record in records if record.get('commodity')))

    return render_template('district_procurement.html', records=records, seasons=seasons,
                         districts=districts, commodities=commodities,
                         selected_season=season, selected_district=district, selected_commodity=commodity)

@district_procurement_bp.route('/api/data')
def api_data():
    season = request.args.get('season', '')
    district = request.args.get('district', '')
    commodity = request.args.get('commodity', '')

    params = {'api-key': DISTRICT_API_KEY, 'format': 'json', 'limit': 1000}
    if season:
        params['filters[season]'] = season
    if district:
        params['filters[district]'] = district
    if commodity:
        params['filters[commodity]'] = commodity

    try:
        response = requests.get(DISTRICT_API_URL, params=params, timeout=10)
        data = response.json()
        return jsonify(data.get('records', []))
    except:
        return jsonify([])

application.register_blueprint(district_procurement_bp, url_prefix='/district_procurement')

crop_price_tracker_bp = Blueprint('crop_price_tracker', __name__,
                                     static_folder=os.path.join('Crop_Prices_Tracker', 'static'),
                                     static_url_path='/static')

@crop_price_tracker_bp.route('/')
@crop_price_tracker_bp.route('/crop_price_tracker', methods=['GET', 'POST'])
def index():
    try:
        crops = sorted({record['commodity'] for record in CROP_DATA if record.get('commodity')})
        result = []
        error = None

        if request.method == 'POST':
            crop = request.form.get('crop', '').strip()
            state = request.form.get('state', '').strip()
            market = request.form.get('market', '').strip()

            if crop and state and market:
                result = [r for r in CROP_DATA if r.get('commodity', '').lower() == crop.lower() and r.get('state', '').lower() == state.lower() and r.get('market', '').lower() == market.lower()]
                if not result:
                    error = "No data found for the given crop, state, and market."
            else:
                error = "All fields are required."

        return render_template('crop_price_tracker.html', crops=crops, result=result, error=error)
    except Exception as e:
        return f"Error: {str(e)}", 500

@crop_price_tracker_bp.route('/get_states')
def get_states():
    crop = request.args.get('crop', '').strip().lower()
    if not crop:
        return jsonify([])
    states = sorted({r['state'] for r in CROP_DATA if r.get('commodity', '').lower() == crop})
    return jsonify(states)

@crop_price_tracker_bp.route('/get_markets')
def get_markets():
    crop = request.args.get('crop', '').strip().lower()
    state = request.args.get('state', '').strip().lower()
    if not crop or not state:
        return jsonify([])
    markets = sorted({r['market'] for r in CROP_DATA if r.get('commodity', '').lower() == crop and r.get('state', '').lower() == state})
    return jsonify(markets)

application.register_blueprint(crop_price_tracker_bp, url_prefix='/crop_price_tracker')

@application.route('/Crop_Prices_Tracker/templates/crop_price_tracker.html')
def crop_price_tracker_direct():
    return render_template('crop_price_tracker.html', crops=sorted({record['commodity'] for record in CROP_DATA if record.get('commodity')}), result=[], error=None)

@application.route('/Crop_Prices_Tracker/templates/crop_price_tracker_telugu.html')
def crop_price_tracker_telugu():
    return render_template('crop_price_tracker_telugu.html')

@application.route('/cropCalendar.html')
def crop_calendar():
    return render_template('cropCalendar.html')

@application.route('/feed-back.html')
def feedback():
    return render_template('feed-back.html')

if __name__ == '__main__':
    application.run(debug=True)
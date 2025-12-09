from flask import Flask, render_template, send_from_directory, redirect, request, jsonify, Blueprint, send_file, abort
import os
import re
import requests
import sys
from functools import wraps
from io import BytesIO
from datetime import datetime
import joblib
import numpy as np

sys.path.append(os.path.join(os.getcwd(), 'Crop_Yield_Prediction', 'crop_yield_app'))

from crop_recommendation_blueprint import crop_recommendation_bp
from crop_price_tracker_blueprint import crop_price_tracker_bp
from Crop_Yield_Prediction.crop_yield_app.crop_yield_blueprint import crop_yield_bp
from labour_alerts_blueprint import labour_alerts_bp
from Crop_Planning.crop_planning_blueprint import crop_planning_bp
from forum_loan_blueprint import forum_loan_bp
from sugarcane_frp_blueprint import sugarcane_frp_bp
from district_procurement_blueprint import district_procurement_bp

application = Flask(__name__, static_folder='static', template_folder='.')

# Add default test user for login testing
if not hasattr(application, 'users'):
    application.users = {}
application.users['test@example.com'] = {'password': 'test123', 'role': 'user', 'fullname': 'Test User'}



application.register_blueprint(crop_price_tracker_bp, url_prefix='/crop_price_tracker')
application.register_blueprint(crop_yield_bp, url_prefix='/crop_yield')
application.register_blueprint(labour_alerts_bp, url_prefix='/labour_alerts')
application.register_blueprint(crop_planning_bp, url_prefix='/crop_planning')
application.register_blueprint(forum_loan_bp, url_prefix='/forum_loan')
application.register_blueprint(crop_recommendation_bp, url_prefix='/crop_recommendation')
application.register_blueprint(sugarcane_frp_bp, url_prefix='/sugarcane_frp')
application.register_blueprint(district_procurement_bp, url_prefix='/district_procurement')

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
def cropplan():
    return render_template('Crop_Planning/templates/cropplan.html')

@application.route('/Labour_Alerts/templates/labour.html')
def labour():
    return render_template('Labour_Alerts/templates/labour.html')

@application.route('/Labour_Alerts/templates/labour_telugu.html')
def labour_telugu():
    return render_template('Labour_Alerts/templates/labour_telugu.html')

@application.route('/Forum/forum.html')
def forum():
    return render_template('Forum/forum.html')

@application.route('/Forum/forum_telugu.html')
def forum_telugu():
    return render_template('Forum/forum_telugu.html')

@application.route('/Crop_Prices_Tracker/templates/crop_price_tracker.html')
def crop_price_tracker():
    return render_template('Crop_Prices_Tracker/templates/crop_price_tracker.html')

@application.route('/Crop_Prices_Tracker/templates/crop_price_tracker_telugu.html')
def crop_price_tracker_telugu():
    return render_template('Crop_Prices_Tracker/templates/crop_price_tracker_telugu.html')

@application.route('/cropCalendar.html')
def crop_calendar():
    return render_template('cropCalendar.html')

@application.route('/feed-back.html')
def feedback():
    return render_template('feed-back.html')

# Sample data for crop states and markets
crop_states = {
    'Wheat': ['Punjab', 'Haryana', 'Uttar Pradesh'],
    'Rice': ['West Bengal', 'Tamil Nadu', 'Andhra Pradesh'],
    'Maize': ['Karnataka', 'Maharashtra', 'Telangana']
}

state_markets = {
    'Punjab': ['Amritsar', 'Ludhiana', 'Jalandhar'],
    'Haryana': ['Karnal', 'Panipat', 'Ambala'],
    'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Varanasi'],
    'West Bengal': ['Kolkata', 'Siliguri', 'Durgapur'],
    'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai'],
    'Andhra Pradesh': ['Vijayawada', 'Visakhapatnam', 'Guntur'],
    'Karnataka': ['Bangalore', 'Mysore', 'Hubli'],
    'Maharashtra': ['Mumbai', 'Pune', 'Nagpur'],
    'Telangana': ['Hyderabad', 'Warangal', 'Nizamabad']
}

@application.route('/crop_price_tracker/get_states')
def get_states():
    crop = request.args.get('crop')
    states = crop_states.get(crop, [])
    return jsonify(states)

@application.route('/crop_price_tracker/get_markets')
def get_markets():
    state = request.args.get('state')
    markets = state_markets.get(state, [])
    return jsonify(markets)

@application.route('/crop_price_tracker/track_prices', methods=['POST'])
def track_prices():
    # This route will be deprecated in favor of AJAX get_prices endpoint
    crop = request.form.get('crop')
    state = request.form.get('state')
    market = request.form.get('market')

    # Mock sample price results
    sample_results = [
        {'arrival_date': '2024-06-01', 'market': market, 'state': state, 'modal_price': 1500},
        {'arrival_date': '2024-06-02', 'market': market, 'state': state, 'modal_price': 1520},
        {'arrival_date': '2024-06-03', 'market': market, 'state': state, 'modal_price': 1490},
    ]

    return render_template('Crop_Prices_Tracker/templates/crop_price_tracker.html', crops=crop_states.keys(), result=sample_results)

@application.route('/crop_price_tracker/get_prices')
def get_prices():
    crop = request.args.get('crop')
    state = request.args.get('state')
    market = request.args.get('market')

    # Validate inputs
    if not crop or not state or not market:
        return jsonify({'error': 'Missing required parameters'}), 400

    # Mock sample price results
    sample_results = [
        {'arrival_date': '2024-06-01', 'market': market, 'state': state, 'modal_price': 1500},
        {'arrival_date': '2024-06-02', 'market': market, 'state': state, 'modal_price': 1520},
        {'arrival_date': '2024-06-03', 'market': market, 'state': state, 'modal_price': 1490},
    ]

    return jsonify(sample_results)

if __name__ == '__main__':
    application.run(debug=True, port=5000)

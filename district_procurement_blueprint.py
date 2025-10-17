from flask import Blueprint, render_template, request, jsonify
import requests

district_procurement_bp = Blueprint('district_procurement', __name__, template_folder='District_Procurement/templates', static_folder='District_Procurement/static')

API_URL = "https://api.data.gov.in/resource/3938e80b-28ce-42d8-b9e8-b8fa0a802172"
API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"  # Sample key

@district_procurement_bp.route('/')
def index():
    season = request.args.get('season', '')
    district = request.args.get('district', '')
    commodity = request.args.get('commodity', '')

    # Fetch data from API
    params = {
        'api-key': API_KEY,
        'format': 'json',
        'limit': 1000  # Adjust as needed
    }

    if season:
        params['filters[season]'] = season
    if district:
        params['filters[district]'] = district
    if commodity:
        params['filters[commodity]'] = commodity

    try:
        response = requests.get(API_URL, params=params)
        data = response.json()
        records = data.get('records', [])
    except:
        records = []

    # Get unique values for filters
    seasons = sorted(set(record.get('season', '') for record in records if record.get('season')))
    districts = sorted(set(record.get('district', '') for record in records if record.get('district')))
    commodities = sorted(set(record.get('commodity', '') for record in records if record.get('commodity')))

    return render_template('district_procurement.html',
                         records=records,
                         seasons=seasons,
                         districts=districts,
                         commodities=commodities,
                         selected_season=season,
                         selected_district=district,
                         selected_commodity=commodity)

@district_procurement_bp.route('/api/data')
def api_data():
    season = request.args.get('season', '')
    district = request.args.get('district', '')
    commodity = request.args.get('commodity', '')

    params = {
        'api-key': API_KEY,
        'format': 'json',
        'limit': 1000
    }

    if season:
        params['filters[season]'] = season
    if district:
        params['filters[district]'] = district
    if commodity:
        params['filters[commodity]'] = commodity

    try:
        response = requests.get(API_URL, params=params)
        data = response.json()
        return jsonify(data.get('records', []))
    except:
        return jsonify([])

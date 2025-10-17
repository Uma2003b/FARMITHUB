from flask import Blueprint, request, jsonify, render_template, current_app
import google.generativeai as genai
import json
import re
from functools import wraps

crop_planning_bp = Blueprint('crop_planning', __name__,
                             template_folder='templates',
                             static_folder='static')

API_KEY = "AIzaSyC4MuJYakQd4T-T74c6kfZ9KBpZNzukJ8Q"

# Input validation helper functions
def sanitize_input(text, max_length=255):
    """Sanitize text input"""
    if not isinstance(text, str):
        return ""
    # Remove potentially dangerous characters
    cleaned = re.sub(r'[<>"\']', '', text.strip())
    return cleaned[:max_length]

def validate_required_fields(required_fields):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            json_data = request.get_json()
            if not json_data:
                return jsonify({'error': 'Invalid JSON data'}), 400
            for field in required_fields:
                if field not in json_data or not json_data[field].strip():
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_user_data(data):
    """Validate user input data"""
    required_fields = ['season', 'Soil_Type']
    for field in required_fields:
        if field not in data or not data[field].strip():
            return False, f"Missing required field: {field}"

    # Validate field lengths
    for field, value in data.items():
        if len(value) > 100:
            return False, f"{field} too long (max 100 characters)"

    return True, "Valid"

# Static data for crop planning (at least 10 scenarios)
static_crop_data = [
    {
        'season': 'Monsoon',
        'soil_type': 'Loamy',
        'climate': 'Tropical',
        'water_availability': 'High',
        'predicted_crop': 'Rice',
        'title': 'Rice Farming Guide',
        'how_to_plant': 'Prepare the field by plowing and leveling.\nSow seeds in nurseries or directly.\nTransplant seedlings after 20-30 days.\nMaintain water level.',
        'fertilizer': 'Use NPK 10-26-26 at planting, urea for top dressing.',
        'timeline': '3-6 months from sowing to harvest.',
        'ideal_rainfall': '1000-2000 mm annually.',
        'post_harvest': 'Dry grains, thresh, and store in cool place.'
    },
    {
        'season': 'Winter',
        'soil_type': 'Sandy',
        'climate': 'Temperate',
        'water_availability': 'Medium',
        'predicted_crop': 'Wheat',
        'title': 'Wheat Farming Guide',
        'how_to_plant': 'Till the soil and sow seeds in rows.\nEnsure proper spacing.\nIrrigate as needed.',
        'fertilizer': 'Apply DAP and urea.',
        'timeline': '4-5 months.',
        'ideal_rainfall': '500-700 mm.',
        'post_harvest': 'Harvest when grains are hard, thresh and store.'
    },
    {
        'season': 'Summer',
        'soil_type': 'Clay',
        'climate': 'Arid',
        'water_availability': 'Low',
        'predicted_crop': 'Maize',
        'title': 'Maize Farming Guide',
        'how_to_plant': 'Plant seeds in hills.\nWater regularly in dry conditions.',
        'fertilizer': 'Use NPK fertilizers.',
        'timeline': '3-4 months.',
        'ideal_rainfall': '400-600 mm.',
        'post_harvest': 'Harvest cobs, dry and shell.'
    },
    {
        'season': 'Monsoon',
        'soil_type': 'Black',
        'climate': 'Tropical',
        'water_availability': 'High',
        'predicted_crop': 'Cotton',
        'title': 'Cotton Farming Guide',
        'how_to_plant': 'Sow seeds in prepared beds.\nThin seedlings.',
        'fertilizer': 'Apply potash and phosphorus.',
        'timeline': '5-6 months.',
        'ideal_rainfall': '600-1000 mm.',
        'post_harvest': 'Pick bolls, gin and bale.'
    },
    {
        'season': 'Winter',
        'soil_type': 'Loamy',
        'climate': 'Subtropical',
        'water_availability': 'Medium',
        'predicted_crop': 'Sugarcane',
        'title': 'Sugarcane Farming Guide',
        'how_to_plant': 'Plant setts in furrows.\nIrrigate frequently.',
        'fertilizer': 'Use nitrogen-rich fertilizers.',
        'timeline': '10-12 months.',
        'ideal_rainfall': '1500-2500 mm.',
        'post_harvest': 'Harvest stalks, crush for juice.'
    },
    {
        'season': 'Summer',
        'soil_type': 'Sandy',
        'climate': 'Arid',
        'water_availability': 'Low',
        'predicted_crop': 'Sorghum',
        'title': 'Sorghum Farming Guide',
        'how_to_plant': 'Sow seeds in rows.\nDrought tolerant.',
        'fertilizer': 'Minimal, use organic.',
        'timeline': '3-4 months.',
        'ideal_rainfall': '300-500 mm.',
        'post_harvest': 'Thresh and store grains.'
    },
    {
        'season': 'Monsoon',
        'soil_type': 'Clay',
        'climate': 'Tropical',
        'water_availability': 'High',
        'predicted_crop': 'Banana',
        'title': 'Banana Farming Guide',
        'how_to_plant': 'Plant suckers in pits.\nMulch and water.',
        'fertilizer': 'Potassium rich.',
        'timeline': '9-12 months.',
        'ideal_rainfall': '2000-2500 mm.',
        'post_harvest': 'Harvest bunches when ripe.'
    },
    {
        'season': 'Winter',
        'soil_type': 'Loamy',
        'climate': 'Temperate',
        'water_availability': 'Medium',
        'predicted_crop': 'Potato',
        'title': 'Potato Farming Guide',
        'how_to_plant': 'Plant tubers in ridges.\nHill soil around.',
        'fertilizer': 'Balanced NPK.',
        'timeline': '2-3 months.',
        'ideal_rainfall': '500-700 mm.',
        'post_harvest': 'Dig tubers, cure and store.'
    },
    {
        'season': 'Summer',
        'soil_type': 'Black',
        'climate': 'Subtropical',
        'water_availability': 'Low',
        'predicted_crop': 'Groundnut',
        'title': 'Groundnut Farming Guide',
        'how_to_plant': 'Sow seeds in rows.\nIrrigate sparingly.',
        'fertilizer': 'Phosphorus and calcium.',
        'timeline': '4-5 months.',
        'ideal_rainfall': '600-1000 mm.',
        'post_harvest': 'Uproot plants, dry pods.'
    },
    {
        'season': 'Monsoon',
        'soil_type': 'Sandy',
        'climate': 'Tropical',
        'water_availability': 'High',
        'predicted_crop': 'Soybean',
        'title': 'Soybean Farming Guide',
        'how_to_plant': 'Inoculate seeds and sow.\nControl weeds.',
        'fertilizer': 'Nitrogen fixing, minimal external.',
        'timeline': '3-4 months.',
        'ideal_rainfall': '700-1200 mm.',
        'post_harvest': 'Harvest pods, thresh.'
    }
]

def clean_ai_response(text_response):
    start = text_response.find('{')
    end = text_response.rfind('}')
    if start != -1 and end != -1:
        return text_response[start:end+1]
    return text_response

def get_ai_prediction_and_guide(user_data):
    if not genai_model:
        return json.dumps({"error": "AI model is not configured."})

    # Sanitize user data before sending to AI
    sanitized_data = {k: sanitize_input(v, 100) for k, v in user_data.items()}
    conditions = ", ".join([f"{key.replace('_', ' ')}: {value}" for key, value in sanitized_data.items()])

    # FINAL, MOST STRICT PROMPT
    prompt = f"""
    You are a JSON API that provides agricultural advice.
    Your entire response MUST be a single, valid JSON object and nothing else.
    
    Analyze these farming conditions: {conditions}
    
    1.  Determine the single best crop that is appropriate for the "Season" provided.
    2.  Generate a farming guide for that crop. **IMPORTANT: For any lists or steps, use the newline character `\\n` to separate items.**
    
    Return a single JSON object with these exact keys: 
    "predicted_crop", "title", "how_to_plant", "fertilizer", "timeline", "ideal_rainfall", "post_harvest".
    """
    
    try:
        response = genai_model.generate_content(prompt)
        return response.text
    except Exception as e:
        current_app.logger.error(f"Error generating content from Gemini: {e}")
        return json.dumps({"error": "Failed to generate AI guide."})

@crop_planning_bp.route('/')
def home():
    return render_template('cropplan.html')

@crop_planning_bp.route('/predict', methods=['POST'])
@validate_required_fields(['data'])
def predict():
    try:
        # Validate content type
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        json_data = request.get_json()
        user_input_data = json_data['data']
        
        # Validate user data
        is_valid, message = validate_user_data(user_input_data)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Sanitize user data
        sanitized_data = {k: sanitize_input(v, 100) for k, v in user_input_data.items()}

        # Find matching static data (match on season and soil_type for now, since form provides those)
        matched_data = None
        for data in static_crop_data:
            if (data['season'].lower() == sanitized_data.get('season', '').lower() and
                data['soil_type'].lower() == sanitized_data.get('Soil_Type', '').lower()):
                matched_data = data
                break

        if matched_data:
            guide_dict = {k: v for k, v in matched_data.items() if k not in ['season', 'soil_type', 'climate', 'water_availability']}
            guide_json_string = json.dumps(guide_dict)
            return jsonify({
                'crop': matched_data['predicted_crop'],
                'guide_json_string': guide_json_string
            })
        else:
            # Default response if no match
            default_guide = {
                'predicted_crop': 'General Crop',
                'title': 'General Farming Guide',
                'how_to_plant': 'Prepare soil and plant seeds appropriately.',
                'fertilizer': 'Use balanced fertilizers.',
                'timeline': 'Varies by crop.',
                'ideal_rainfall': 'Depends on crop.',
                'post_harvest': 'Harvest and store properly.'
            }
            return jsonify({
                'crop': 'General Crop',
                'guide_json_string': json.dumps(default_guide)
            })

    except Exception as e:
        current_app.logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': 'Prediction failed'}), 500

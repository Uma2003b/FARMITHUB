from flask import Flask, request, jsonify
import google.generativeai as genai
import traceback
import os
import re
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from crop_yield_blueprint import crop_yield_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

app.register_blueprint(crop_yield_bp, url_prefix='/crop_yield')

# In-memory storage for forum posts (in production, use a database)
forum_posts = []

# Input validation and sanitization functions
def sanitize_input(text):
    """Sanitize user input to prevent XSS and injection attacks"""
    if not text or not isinstance(text, str):
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Escape special characters
    text = text.replace('&', '&amp;')
    text = text.replace('<', '<')
    text = text.replace('>', '>')
    text = text.replace('"', '"')
    text = text.replace("'", '&#x27;')
    
    # Limit length
    if len(text) > 1000:
        text = text[:1000]
    
    return text.strip()

def validate_input(data):
    """Validate input data structure and content"""
    if not data:
        return False, "No data provided"
    
    # Check for required fields if needed
    # Add specific validation rules here
    
    return True, "Valid input"

# Initialize Gemini API
API_KEY = os.environ.get('GEMINI_API_KEY', 'YOUR-API-KEY')
MODEL_ID = 'gemini-1.5-flash'

# Configure Gemini Client
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_ID)


@app.route('/api/firebase-config')
def get_firebase_config():
    """Secure endpoint to provide Firebase configuration to client"""
    return jsonify({
        'apiKey': os.environ.get('FIREBASE_API_KEY'),
        'authDomain': os.environ.get('FIREBASE_AUTH_DOMAIN'),
        'projectId': os.environ.get('FIREBASE_PROJECT_ID'),
        'storageBucket': os.environ.get('FIREBASE_STORAGE_BUCKET'),
        'messagingSenderId': os.environ.get('FIREBASE_MESSAGING_SENDER_ID'),
        'appId': os.environ.get('FIREBASE_APP_ID'),
        'measurementId': os.environ.get('FIREBASE_MEASUREMENT_ID')
    })


@app.route('/process-loan', methods=['POST'])
def process_loan():
    try:
        json_data = request.get_json(force=True)
        
        # Validate and sanitize input
        is_valid, validation_message = validate_input(json_data)
        if not is_valid:
            return jsonify({"status": "error", "message": validation_message}), 400
        
        # Sanitize any text fields in the JSON data
        if isinstance(json_data, dict):
            for key, value in json_data.items():
                if isinstance(value, str):
                    json_data[key] = sanitize_input(value)
        
        print(f"Received JSON: {json_data}")

        prompt = f"""
You are a financial loan eligibility advisor specializing in agricultural loans for farmers in India.

You will be given a JSON object that contains information about a farmer's loan application. The fields in this JSON will vary depending on the loan type (e.g., Crop Cultivation, Farm Equipment, Water Resources, Land Purchase).
You will focus only on loan schemes and eligibility criteria followed by:
1. Indian nationalized banks (e.g., SBI, Bank of Baroda)
2. Private sector Indian banks (e.g., ICICI, HDFC)
3. Regional Rural Banks (RRBs)
4. Cooperative Banks
5. NABARD & government schemes
Do not suggest generic or international financing options.

JSON Data = {json_data}

Your task is to:
1. Identify the loan type and understand which fields are important for assessing that particular loan.
2. Analyze the farmer's provided details and assess their loan eligibility.
3. Highlight areas of strength and areas where the farmer may face challenges.
4. If any critical data is missing from the JSON, point it out clearly.
5. Provide simple and actionable suggestions the farmer can follow to improve eligibility.
6. Suggest the government schemes or subsidies applicable to their loan type.
7. Ensure the tone is clear, supportive, and easy to understand for farmers.
8. Respond in a structured format with labeled sections: Loan Type, Eligibility Status, Loan Range, Improvements, Schemes.
9. **IMPORTANT: Return your response in **Markdown format** with:
Headings for each section (Loan Type, Eligibility Status, Loan Range, Improvements, Schemes)
Bullet points ( - ) for lists.
Do not use "\\n" for newlines. Instead, structure properly.

Do not add assumptions that are not supported by the data provided.
"""

        response = model.generate(
            prompt=prompt,
            temperature=0.7,
            max_output_tokens=1024
        )

        reply = response.candidates[0].message.content
        return jsonify({"status": "success", "message": reply}), 200

    except Exception as e:
        print(f"Unexpected Error: {e}")
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/forum', methods=['GET'])
def get_forum_posts():
    """Get all forum posts"""
    return jsonify(forum_posts)


@app.route('/forum', methods=['POST'])
def add_forum_post():
    """Add a new forum post"""
    try:
        data = request.get_json()
        if not data or 'name' not in data or 'message' not in data:
            return jsonify({"error": "Name and message are required"}), 400
        
        # Sanitize inputs
        name = sanitize_input(data['name'])
        message = sanitize_input(data['message'])
        
        post = {
            'id': len(forum_posts) + 1,
            'name': name,
            'message': message,
            'timestamp': os.times()  # Simple timestamp
        }
        forum_posts.append(post)
        return jsonify(post), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


from flask import send_from_directory
import os

@app.route('/')
def serve_index():
    return send_from_directory('', 'index.html')

import os

@app.route('/organic_telugu.html')
def serve_organic_telugu():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, 'organic_telugu.html')
    print(f"Serving organic_telugu.html from: {file_path}")
    if os.path.exists(file_path):
        return send_from_directory(base_dir, 'organic_telugu.html')
    else:
        print("File not found at expected location.")
        return "File not found", 404

@app.route('/<path:path>')
def serve_static_file(path):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, path)
    if os.path.exists(file_path):
        return send_from_directory(base_dir, path)
    else:
        return "File not found", 404


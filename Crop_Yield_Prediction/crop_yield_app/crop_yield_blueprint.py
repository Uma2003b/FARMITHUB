from flask import Blueprint, render_template, request, jsonify, send_file, redirect
import joblib
import numpy as np
import os
import logging
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

basedir = os.path.abspath(os.path.dirname(__file__))

crop_yield_bp = Blueprint('crop_yield', __name__, template_folder=os.path.join(basedir, 'templates'))

# Logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("farmit")

# Load model and encoders (fail fast with clear errors)
try:
    model = joblib.load(os.path.join(basedir, 'models', 'xgb_crop_model.pkl'))
    crop_encoder = joblib.load(os.path.join(basedir, 'models', 'Crop_encoder.pkl'))
    season_encoder = joblib.load(os.path.join(basedir, 'models', 'Season_encoder.pkl'))
    state_encoder = joblib.load(os.path.join(basedir, 'models', 'State_encoder.pkl'))
    log.info("Model & encoders loaded.")
except Exception as e:
    log.exception("Failed to load model/encoders.")
    raise

CROPS = [
    "Rice", "Wheat", "Maize", "Soyabean", "Cotton(lint)", "Sugarcane", "Groundnut", "Potato",
    "Barley", "Jowar", "Bajra", "Ragi", "Arhar/Tur", "Moong(Green Gram)", "Urad", "Gram",
    "Peas & beans (Pulses)", "Rapeseed &Mustard", "Sunflower", "Safflower", "Sesamum", "Linseed", "Castor seed", "Coconut ",
    "Jute", "Mesta", "Tobacco", "Arecanut", "Banana", "Onion", "Garlic", "Ginger",
    "Turmeric", "Coriander", "Dry chillies", "Black pepper", "Cardamom", "Cashewnut"
]

STATES = [
    "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa",
    "Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka","Kerala",
    "Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland",
    "Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura",
    "Uttar Pradesh","Uttarakhand","West Bengal"
]

SEASONS = ["Kharif     ","Rabi       ","Whole Year ","Autumn     ","Summer     ","Winter     "]

@crop_yield_bp.route("/")
def index():
    return render_template("index_fixed.html", crops=CROPS, states=STATES, seasons=SEASONS)

@crop_yield_bp.route('/yield_prediction')
def yield_prediction_redirect():
    return redirect('/crop_yield/')

@crop_yield_bp.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return redirect('/crop_yield/')
    try:
        data = [
            request.form['crop'],
            int(request.form['year']),
            request.form['season'],
            request.form['state'],
            float(request.form['area']),
            float(request.form['rainfall']),
            float(request.form['production'])
        ]

        input_params = {
            'crop': request.form['crop'],
            'year': request.form['year'],
            'season': request.form['season'],
            'state': request.form['state'],
            'area': request.form['area'],
            'production': request.form['production'],
            'rainfall': request.form['rainfall']
        }

        # Handle encoding with proper error handling
        try:
            crop_encoded = crop_encoder.transform([data[0]])[0]
        except ValueError:
            # If crop not found, use the first available crop
            crop_encoded = 0
            
        try:
            season_encoded = season_encoder.transform([data[2]])[0]
        except ValueError:
            # If season not found, use the first available season
            season_encoded = 0
            
        try:
            state_encoded = state_encoder.transform([data[3]])[0]
        except ValueError:
            # If state not found, use the first available state
            state_encoded = 0

        # NOTE: order must match what your model expects
        features = np.array([[crop_encoded, data[1], season_encoded, state_encoded, data[4], data[5], data[6]]])

        pred_val = float(model.predict(features)[0])
        # Ensure prediction is positive and reasonable
        prediction = max(0.1, round(pred_val, 2))

        return render_template('yield_result.html', prediction=prediction, params=input_params)
    except Exception as e:
        error_message = str(e)
        return render_template('yield_result.html', error=error_message)

@crop_yield_bp.route("/api/crops")
def get_crops():
    return jsonify(crops=CROPS)

@crop_yield_bp.route("/api/states")
def get_states():
    return jsonify(states=STATES)

@crop_yield_bp.route("/api/seasons")
def get_seasons():
    return jsonify(seasons=SEASONS)

@crop_yield_bp.route('/download_report', methods=['POST'])
def download_report():
    try:
        prediction = request.form['prediction']
        params = {
            'crop': request.form['crop'],
            'year': request.form['year'],
            'season': request.form['season'],
            'state': request.form['state'],
            'area': request.form['area'],
            'production': request.form['production'],
            'rainfall': request.form['rainfall']
        }
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        p.setFont('Helvetica-Bold', 20)
        p.drawString(50, height - 50, "FARMIT HUB - Crop Yield Report")
        p.setFont('Helvetica', 12)
        p.drawString(50, height - 80, f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")

        p.setFont('Helvetica-Bold', 14)
        p.drawString(50, height - 120, "Yield Prediction:")
        p.setFont('Helvetica', 12)
        p.drawString(50, height - 140, f"Predicted Yield: {prediction} tonnes/hectare")

        p.setFont('Helvetica-Bold', 14)
        p.drawString(50, height - 180, "Input Parameters:")
        p.setFont('Helvetica', 12)
        y = height - 200
        for k, v in params.items():
            p.drawString(70, y, f"{k.title()}: {v}")
            y -= 20

        p.showPage()
        p.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f"yield_prediction_report.pdf", mimetype='application/pdf')
    except Exception as e:
        return f"Error generating PDF: {e}"

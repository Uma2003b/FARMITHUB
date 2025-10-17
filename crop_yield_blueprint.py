from flask import Blueprint, render_template, request, jsonify, send_file, redirect
import joblib
import numpy as np
import os
import logging
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

basedir = os.path.join(os.getcwd(), 'Crop_Yield_Prediction', 'crop_yield_app')

crop_yield_bp = Blueprint('crop_yield', __name__, template_folder=os.path.join(basedir, 'templates'))

# Logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("farmit")

# Load model and encoders (fail fast with clear errors)
try:
    model = joblib.load(os.path.join(os.getcwd(), 'yield_predictor_model.pkl'))
    crop_encoder = joblib.load(os.path.join(os.getcwd(), 'area_encoder.pkl'))
    season_encoder = joblib.load(os.path.join(os.getcwd(), 'item_encoder.pkl'))
    state_encoder = joblib.load(os.path.join(os.getcwd(), 'item_encoder.pkl'))  # Assuming same encoder
    log.info("Model & encoders loaded.")
except Exception as e:
    log.exception("Failed to load model/encoders.")
    raise

CROPS = [
    "Rice","Wheat","Maize","Soyabean","Cotton","Sugarcane","Groundnut","Potato",
    "Barley","Jowar","Bajra","Ragi","Tur","Moong","Urad","Gram","Peas",
    "Mustard","Sunflower","Safflower","Sesamum","Linseed","Castor","Coconut",
    "Jute","Mesta","Tobacco","Arecanut","Banana","Mango","Grapes","Orange",
    "Papaya","Pomegranate","Guava","Apple","Litchi","Ber","Sapota"
]

STATES = [
    "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa",
    "Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka","Kerala",
    "Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland",
    "Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura",
    "Uttar Pradesh","Uttarakhand","West Bengal"
]

SEASONS = ["Kharif","Rabi","Whole Year","Autumn","Summer","Winter"]

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
        # Ensure this route is only called from crop_yield blueprint form
        if request.referrer and '/crop_yield' not in request.referrer:
            return redirect('/crop_yield/')
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

        # Fix for unseen labels: fit encoders with known classes before transform
        crop_encoder_classes = crop_encoder.classes_.tolist()
        if data[0] not in crop_encoder_classes:
            crop_encoder.classes_ = np.append(crop_encoder.classes_, data[0])
        crop_encoded = crop_encoder.transform([data[0]])[0]

        season_encoder_classes = season_encoder.classes_.tolist()
        if data[2] not in season_encoder_classes:
            season_encoder.classes_ = np.append(season_encoder.classes_, data[2])
        season_encoded = season_encoder.transform([data[2]])[0]

        state_encoder_classes = state_encoder.classes_.tolist()
        if data[3] not in state_encoder_classes:
            state_encoder.classes_ = np.append(state_encoder.classes_, data[3])
        state_encoded = state_encoder.transform([data[3]])[0]

        # Adjust features to match model input (5 features expected)
        # According to training script, features are: area_encoded, item_encoded, average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp
        # Map input accordingly:
        # data indices: crop_encoded (item_encoded), year (not used), season_encoded (not used), state_encoded (not used), area, rainfall, production (not used)
        features = np.array([[data[4], crop_encoded, data[5], data[6], 25.0]])  # 25.0 as placeholder for avg_temp or adjust as needed

        pred_val = float(model.predict(features)[0])
        prediction = round(pred_val, 2)

        return render_template('result.html', prediction=prediction, params=input_params)
    except Exception as e:
        error_message = str(e)
        return render_template('result.html', error=error_message)

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

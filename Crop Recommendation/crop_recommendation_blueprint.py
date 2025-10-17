from flask import Blueprint, render_template, request, send_file
import joblib
import numpy as np
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import logging

crop_recommendation_bp = Blueprint('crop_recommendation', __name__, template_folder='templates', static_folder='static')
logger = logging.getLogger(__name__)

# Load model and label encoder
model = joblib.load('model/rf_model.pkl')
le = joblib.load('model/label_encoder.pkl')

@crop_recommendation_bp.route('/')
def home():
    return render_template('crop_recommendation.html')

@crop_recommendation_bp.route('/predict', methods=['POST'])
def predict():
    try:
        # Log all form data received
        logger.info(f"Form data received: {request.form}")

        # Get form data
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        logger.info(f"Predict request: N={N}, P={P}, K={K}, temp={temperature}, hum={humidity}, ph={ph}, rain={rainfall}")

        # Prepare input for model
        input_data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])

        # Predict
        prediction = model.predict(input_data)
        crop = le.inverse_transform(prediction)[0]

        logger.info(f"Prediction result: {crop}")

        # Prepare params for template
        params = {
            'N': N,
            'P': P,
            'K': K,
            'temperature': temperature,
            'humidity': humidity,
            'ph': ph,
            'rainfall': rainfall,
            'soil_type': None  # Not used in this model
        }

        return render_template('result.html', crop=crop, params=params, error=None)

    except Exception as e:
        logger.error(f"Error in prediction: {str(e)}", exc_info=True)
        return render_template('result.html', crop=None, params=None, error=str(e))

@crop_recommendation_bp.route('/download_report', methods=['POST'])
def download_report():
    try:
        # Get data from form
        N = request.form['N']
        P = request.form['P']
        K = request.form['K']
        temperature = request.form['temperature']
        humidity = request.form['humidity']
        ph = request.form['ph']
        rainfall = request.form['rainfall']
        crop = request.form['crop']

        logger.info(f"Generating PDF report for crop: {crop}")

        # Create PDF
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # Title
        c.setFont("Helvetica-Bold", 20)
        c.drawString(200, height - 50, "Crop Recommendation Report")

        # Date
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Parameters
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, height - 120, "Input Parameters:")
        c.setFont("Helvetica", 12)
        y = height - 140
        c.drawString(50, y, f"Nitrogen: {N} kg/ha")
        c.drawString(50, y - 20, f"Phosphorus: {P} kg/ha")
        c.drawString(50, y - 40, f"Potassium: {K} kg/ha")
        c.drawString(50, y - 60, f"Temperature: {temperature} °C")
        c.drawString(50, y - 80, f"Humidity: {humidity} %")
        c.drawString(50, y - 100, f"pH: {ph}")
        c.drawString(50, y - 120, f"Rainfall: {rainfall} mm")

        # Recommendation
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y - 160, "Recommended Crop:")
        c.setFont("Helvetica", 12)
        c.drawString(50, y - 180, crop)

        c.save()
        buffer.seek(0)

        logger.info("PDF report generated successfully")
        return send_file(buffer, as_attachment=True, download_name='crop_recommendation_report.pdf', mimetype='application/pdf')

    except Exception as e:
        logger.error(f"Error generating PDF report: {str(e)}")
        return str(e), 400

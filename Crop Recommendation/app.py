from flask import Flask, render_template, request, send_file, redirect, url_for
import joblib
import numpy as np
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import logging

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crop_recommendation_blueprint import crop_recommendation_bp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(crop_recommendation_bp, url_prefix='')

@app.route('/')
def root():
    logger.info("Root route accessed, redirecting to crop recommendation home")
    return redirect(url_for('crop_recommendation.home'))

if __name__ == '__main__':
    app.run(debug=True, port=5501)

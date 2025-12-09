#!/usr/bin/env python3
import joblib
import numpy as np
import os

# Test model loading
basedir = os.path.abspath(os.path.dirname(__file__))

try:
    print("Loading model and encoders...")
    model = joblib.load(os.path.join(basedir, 'models', 'xgb_crop_model.pkl'))
    crop_encoder = joblib.load(os.path.join(basedir, 'models', 'Crop_encoder.pkl'))
    season_encoder = joblib.load(os.path.join(basedir, 'models', 'Season_encoder.pkl'))
    state_encoder = joblib.load(os.path.join(basedir, 'models', 'State_encoder.pkl'))
    
    print("SUCCESS: Model and encoders loaded successfully!")
    print(f"Model type: {type(model)}")
    print(f"Crop encoder classes: {len(crop_encoder.classes_)} classes")
    print(f"Season encoder classes: {len(season_encoder.classes_)} classes")
    print(f"State encoder classes: {len(state_encoder.classes_)} classes")
    
    # Test prediction with sample data
    print("\nTesting prediction...")
    
    # Sample data: Rice, 2024, Kharif, Punjab, 2.5 hectares, 1200mm rainfall, 10 tonnes production
    crop_encoded = crop_encoder.transform(['Rice'])[0]
    season_encoded = season_encoder.transform(['Kharif     '])[0]
    state_encoded = state_encoder.transform(['Punjab'])[0]
    
    features = np.array([[crop_encoded, 2024, season_encoded, state_encoded, 2.5, 1200, 10]])
    prediction = model.predict(features)[0]
    
    print(f"SUCCESS: Test prediction: {prediction:.2f} tonnes/hectare")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
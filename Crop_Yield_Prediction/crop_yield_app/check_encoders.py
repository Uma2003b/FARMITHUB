#!/usr/bin/env python3
import joblib
import os

basedir = os.path.abspath(os.path.dirname(__file__))

try:
    crop_encoder = joblib.load(os.path.join(basedir, 'models', 'Crop_encoder.pkl'))
    season_encoder = joblib.load(os.path.join(basedir, 'models', 'Season_encoder.pkl'))
    state_encoder = joblib.load(os.path.join(basedir, 'models', 'State_encoder.pkl'))
    
    print("Crop encoder classes:")
    print(crop_encoder.classes_)
    print("\nSeason encoder classes:")
    print(season_encoder.classes_)
    print("\nState encoder classes:")
    print(state_encoder.classes_)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
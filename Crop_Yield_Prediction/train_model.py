#!/usr/bin/env python3
"""
Simple script to train the crop yield prediction model
"""
import os
import sys

# Change to the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

print("Training crop yield prediction model...")
print(f"Working directory: {os.getcwd()}")

# Run the training script
exec(open('crop_yield_predictor.py').read())
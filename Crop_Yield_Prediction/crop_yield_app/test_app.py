#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app import app

if __name__ == "__main__":
    print("Starting Crop Yield Prediction App...")
    print("Access the app at: http://localhost:5502")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, host="0.0.0.0", port=5502)
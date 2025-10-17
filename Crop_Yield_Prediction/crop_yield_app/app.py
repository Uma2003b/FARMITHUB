from flask import Flask
from crop_yield_blueprint import crop_yield_bp
import os

basedir = os.path.abspath(os.path.dirname(__file__))
from flask import redirect

app = Flask(__name__, template_folder=os.path.join(basedir, 'templates'))

app.register_blueprint(crop_yield_bp, url_prefix='/crop_yield')

@app.route('/')
def root_redirect():
    return redirect('/crop_yield/')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5502)

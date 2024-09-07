from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__, static_folder='.')
CORS(app)

# Route to serve the frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'index.html')

# Route to serve static files like JS, CSS, images, etc.
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# API Route to serve forecast data from JSON file
@app.route('/forecast')
def get_forecast():
    # Read forecast data from the JSON file
    json_file_path = os.path.join(os.getcwd(), 'forecasted_covid_data_7_days.json')  # Adjust path as needed
    try:
        with open(json_file_path, 'r') as json_file:
            forecast_data = json.load(json_file)
    except FileNotFoundError:
        return jsonify({"error": "Forecast JSON file not found"}), 404
    
    return jsonify(forecast_data)

# API Route to serve original COVID data from JSON file
@app.route('/original')
def get_original_data():
    # Read original data from the JSON file
    json_file_path = os.path.join(os.getcwd(), 'original_covid_data.json')  # Adjust path as needed
    try:
        with open(json_file_path, 'r') as json_file:
            original_data = json.load(json_file)
    except FileNotFoundError:
        return jsonify({"error": "Original data JSON file not found"}), 404
    
    return jsonify(original_data)

if __name__ == "__main__":
    app.run(debug=True)

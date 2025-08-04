from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from Aclive_Helper import llm


app = Flask(__name__)
CORS(app)

# Example endpoint: Get elevation for a list of coordinates using Open-Elevation API
def get_elevation(lat, lon):
    # Use OpenTopoData API for elevation
    url = f'https://api.opentopodata.org/v1/srtm90m?locations={lat},{lon}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            return data['results'][0].get('elevation')
    return None

@app.route('/elevation', methods=['POST'])
def elevation():
    coords = request.json.get('coordinates', [])
    results = []
    for coord in coords:
        lat, lon = coord['lat'], coord['lon']
        elevation = get_elevation(lat, lon)
        results.append({'lat': lat, 'lon': lon, 'elevation': elevation})
    return jsonify(results)

# Example endpoint: Predict roads with elevation using AI assistant (stub)
@app.route('/predict_roads', methods=['POST'])
def predict_roads():
    data = request.json
    # If a chat message is sent, handle it
    if 'message' in data:
        prompt = data['message']
        analysis = llm(prompt)
        return jsonify({'prediction': analysis, 'input': prompt})
    # If elevations are sent, handle elevation analysis
    elevations = data.get('elevations', [])
    prompt = "Analyze the following elevation data for roads. Identify which roads have significant elevation changes and describe them. Data: "
    prompt += str(elevations)
    analysis = llm(prompt)
    return jsonify({'prediction': analysis, 'input': elevations})

if __name__ == '__main__':
    app.run(debug=True)

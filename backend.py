from flask import Flask, request, jsonify
from Aclive_Helper import llm 

app = Flask(__name__)

# Example endpoint: Get elevation for a list of coordinates using Open-Elevation API
def get_elevation(lat, lon):
    url = f'https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['results'][0]['elevation']
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
    elevations = data.get('elevations', [])
    # Format the elevation data into a prompt for the LLM
    prompt = "Analyze the following elevation data for roads. Identify which roads have significant elevation changes and describe them. Data: "
    prompt += str(elevations)
    # Call the LLM
    analysis = llm(prompt)
    return jsonify({'prediction': analysis, 'input': elevations})

if __name__ == '__main__':
    app.run(debug=True)

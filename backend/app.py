import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# טעינת משתני הסביבה
load_dotenv()
API_KEY = os.getenv("API_KEY")
ENDPOINT = os.getenv("ENDPOINT")

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('image')
    country = request.form.get('country', 'Unknown')

    if not file:
        return jsonify({"error": "No image provided"}), 400

    headers = {
        'Ocp-Apim-Subscription-Key': API_KEY,
        'Content-Type': 'application/octet-stream'
    }
    params = {'returnFaceAttributes': 'age'}
    response = requests.post(f"{ENDPOINT}/face/v1.0/detect", headers=headers, params=params, data=file.read())

    if response.status_code != 200:
        return jsonify({"error": f"Azure API error: {response.text}"}), response.status_code

    result = response.json()
    if not result:
        return jsonify({"error": "No face detected"}), 400

    age = result[0]['faceAttributes']['age']
    return jsonify({"age": age, "country": country, "message": "Analysis successful"})

if __name__ == '__main__':
    app.run(debug=True)

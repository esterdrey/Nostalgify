import base64
import requests
from flask import Flask, render_template, request, jsonify
import os
from io import BytesIO
from PIL import Image

# Azure Face API settings
AZURE_ENDPOINT = "https://nostalgifyapp.cognitiveservices.azure.com/"
AZURE_API_KEY = "2iWX7sQ6mzHvGG18xGJQ2rUgbjInyQiQJ0o9pAB7BaO01c7tOxrAJQQJ99ALACYeBjFXJ3w3AAAKACOGc7zL"
FACE_API_URL = f"{AZURE_ENDPOINT}face/v1.0/detect"

# Flask setup
app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    try:
        data = request.json
        if not data or 'image' not in data or 'country' not in data:
            return jsonify({"error": "Missing 'image' or 'country' in request"}), 400

        image_data = data['image']
        country = data['country']

        # Decode image
        header, encoded = image_data.split(",", 1)
        image_binary = base64.b64decode(encoded)

        # Send image to Azure Face API
        headers = {
            "Ocp-Apim-Subscription-Key": AZURE_API_KEY,
            "Content-Type": "application/octet-stream"
        }
        params = {"returnFaceAttributes": "age"}  # Request age attribute
        response = requests.post(FACE_API_URL, headers=headers, params=params, data=image_binary)

        if response.status_code != 200:
            return jsonify({"error": f"Azure API Error: {response.text}"}), response.status_code

        faces = response.json()
        if not faces:
            return jsonify({"error": "No face detected in the image"}), 400

        # Extract age and count faces
        face_count = len(faces)
        ages = [face['faceAttributes']['age'] for face in faces]

        # Create playlist link
        playlist_link = f"https://open.spotify.com/playlist/dummy_playlist_for_{country}_facecount_{face_count}"

        return jsonify({
            "message": "Face(s) detected successfully",
            "faceCount": face_count,
            "ages": ages,
            "country": country,
            "playlist": playlist_link
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

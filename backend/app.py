from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image
import requests
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# Spotify Authentication
sp = Spotify(auth_manager=SpotifyClientCredentials(client_id="YOUR_CLIENT_ID", client_secret="YOUR_CLIENT_SECRET"))

# Azure Face API Configuration
AZURE_ENDPOINT = "https://nostalgifyapp.cognitiveservices.azure.com"
AZURE_KEY = "2iWX7sQ6mzHvGG18xGJQ2rUgbjInyQiQJ0o9pAB7BaO01c7tOxrAJQQJ99ALACYeBjFXJ3w3AAAKACOGc7zL"

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    image_data = data['image'].split(',')[1]
    country = data['country']

    # Decode image
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_bytes = buffered.getvalue()

    # Send to Azure Face API
    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_KEY,
        'Content-Type': 'application/octet-stream'
    }
    params = {
        'returnFaceAttributes': 'age'
    }
    response = requests.post(f"{AZURE_ENDPOINT}/face/v1.0/detect", headers=headers, params=params, data=image_bytes)
    response.raise_for_status()
    faces = response.json()

    if not faces:
        return jsonify({ 'error': 'No face detected' }), 400

    age = faces[0]['faceAttributes']['age']

    # Generate playlist based on age and country
    query = f"Top hits from the {2023 - int(age) - 10}s in {country}"
    results = sp.search(q=query, type='playlist', limit=1)
    playlist_url = results['playlists']['items'][0]['external_urls']['spotify']

    return jsonify({ 'playlist': playlist_url })

if __name__ == '__main__':
    app.run(debug=True)
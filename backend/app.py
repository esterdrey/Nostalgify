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
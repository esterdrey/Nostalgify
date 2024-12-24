import base64
import requests
from flask import Flask, render_template, request, jsonify
import os
from io import BytesIO
from PIL import Image
from datetime import datetime
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

# הגדרות Azure Face API
AZURE_ENDPOINT = "https://nostalgifyapp.cognitiveservices.azure.com/"
AZURE_API_KEY = "הכנס_את_מפתח_הAPI_כאן"
FACE_API_URL = f"{AZURE_ENDPOINT}face/v1.0/detect"

# הגדרות Spotipy
SPOTIFY_CLIENT_ID = "הכנס_את_ה-Client_ID_שלך"
SPOTIFY_CLIENT_SECRET = "הכנס_את_ה-Client_Secret_שלך"

# אתחול Spotipy
spotify = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# הגדרת Flask
app = Flask(__name__)

@app.route('/')
def home():
    """הצגת עמוד הבית - index.html"""
    return render_template('index.html')

def get_spotify_playlist(decade, country):
    """חיפוש פלייליסט ב-Spotify לפי עשור ומדינה"""
    query = f"top hits {decade} {country}"
    results = spotify.search(q=query, type='playlist', limit=1)
    if results['playlists']['items']:
        return results['playlists']['items'][0]['external_urls']['spotify']
    else:
        return None

@app.route('/process', methods=['POST'])
def process_image():
    """עיבוד תמונה וזיהוי גיל באמצעות Azure Face API ויצירת פלייליסט מותאם"""
    try:
        # קבלת הנתונים מה-Frontend
        data = request.json
        if not data or 'image' not in data or 'country' not in data:
            return jsonify({"error": "Missing 'image' or 'country' in request"}), 400

        image_data = data['image']
        country = data['country']

        # המרת התמונה לבינארי
        header, encoded = image_data.split(",", 1)
        image_binary = base64.b64decode(encoded)

        # שליחת התמונה ל-Azure Face API
        headers = {
            "Ocp-Apim-Subscription-Key": AZURE_API_KEY,
            "Content-Type": "application/octet-stream"
        }
        params = {
            "returnFaceAttributes": "age"
        }

        response = requests.post(FACE_API_URL, headers=headers, params=params, data=image_binary)

        if response.status_code != 200:
            return jsonify({"error": f"Azure API Error: {response.text}"}), response.status_code

        faces = response.json()
        if not faces:
            return jsonify({"error": "No face detected in the image"}), 400

        # ניתוח הגיל
        age = faces[0]['faceAttributes']['age']
        current_year = datetime.now().year
        childhood_year = current_year - int(age) + 10
        decade = (childhood_year // 10) * 10

        # שימוש ב-Spotipy לחיפוש פלייליסט
        playlist_link = get_spotify_playlist(decade, country)
        if not playlist_link:
            return jsonify({"error": "No playlist found"}), 404

        return jsonify({
            "message": "Face and age detected successfully",
            "age": age,
            "decade": decade,
            "country": country,
            "playlist": playlist_link
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

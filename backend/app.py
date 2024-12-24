import base64
import requests
from flask import Flask, render_template, request, jsonify
import os
from io import BytesIO
from PIL import Image
from datetime import datetime

# הגדרות Azure Face API
AZURE_ENDPOINT = "https://nostalgifyapp.cognitiveservices.azure.com/"
AZURE_API_KEY = "2iWX7sQ6mzHvGG18xGJQ2rUgbjInyQiQJ0o9pAB7BaO01c7tOxrAJQQJ99ALACYeBjFXJ3w3AAAKACOGc7zL"
FACE_API_URL = f"{AZURE_ENDPOINT}face/v1.0/detect"

# הגדרת Flask
app = Flask(__name__)

@app.route('/')
def home():
    """הצגת עמוד הבית - index.html"""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    """עיבוד תמונה וזיהוי גיל ויצירת פלייליסט אמיתי מותאם לעשור"""
    try:
        # קבלת הנתונים מה-Frontend
        data = request.json
        if not data or 'image' not in data:
            return jsonify({"error": "Missing 'image' in request"}), 400

        image_data = data['image']

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

        # רשימה של פלייליסטים אמיתיים לפי עשור
        playlists = {
            1950: "https://open.spotify.com/playlist/37i9dQZF1DXaKIA8E7WcJj",
            1960: "https://open.spotify.com/playlist/37i9dQZF1DXbTxeAdrVG2l",
            1970: "https://open.spotify.com/playlist/37i9dQZF1DWTJ7xPn4vNaz",
            1980: "https://open.spotify.com/playlist/37i9dQZF1DX4UtSsGT1Sbe",
            1990: "https://open.spotify.com/playlist/37i9dQZF1DXbTxeAdrVG2l",
            2000: "https://open.spotify.com/playlist/37i9dQZF1DX4o1oenSJRJd",
            2010: "https://open.spotify.com/playlist/37i9dQZF1DX5Ejj0EkURtP",
            2020: "https://open.spotify.com/playlist/37i9dQZF1DX0h0QnLkMBl4"
        }

        # בחירת פלייליסט לפי העשור
        playlist_link = playlists.get(decade, "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M")  # פלייליסט כללי אם אין התאמה

        # החזרת התוצאה
        return jsonify({
            "message": "Face and age detected successfully",
            "age": age,
            "decade": decade,
            "playlist": playlist_link
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

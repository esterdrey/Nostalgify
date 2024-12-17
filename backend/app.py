import base64
import requests
from flask import Flask, render_template, send_from_directory, request, jsonify
import os
from io import BytesIO
from PIL import Image

# הגדרות ה-Azure Face API שלך
AZURE_ENDPOINT = "https://nostalgifyapp.cognitiveservices.azure.com/"
AZURE_API_KEY = "2iWX7sQ6mzHvGG18xGJQ2rUgbjInyQiQJ0o9pAB7BaO01c7tOxrAJQQJ99ALACYeBjFXJ3w3AAAKACOGc7zL"  # החלף במפתח ה-API שלך
FACE_API_URL = f"{AZURE_ENDPOINT}face/v1.0/detect"

# הגדרת Flask
app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')

@app.route('/')
def home():
    """הצגת עמוד הבית - index.html"""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    """עיבוד תמונה וזיהוי פנים באמצעות Azure Face API"""
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

        # שמירת התמונה לבדיקה (אופציונלי)
        temp_image_path = "uploaded_image.png"
        image = Image.open(BytesIO(image_binary))
        image.save(temp_image_path)

        # שליחת התמונה ל-Azure Face API
        headers = {
            "Ocp-Apim-Subscription-Key": AZURE_API_KEY,
            "Content-Type": "application/octet-stream"
        }

        # בקשה לזיהוי פנים בלבד (ללא תכונות נוספות)
        response = requests.post(FACE_API_URL, headers=headers, data=image_binary)

        # בדיקת תגובה
        if response.status_code != 200:
            return jsonify({"error": f"Azure API Error: {response.text}"}), response.status_code

        # עיבוד התגובה מה-Azure
        faces = response.json()
        if not faces:
            return jsonify({"error": "No face detected in the image"}), 400

        # ספירת מספר הפנים שנמצאו
        face_count = len(faces)

        # יצירת לינק לפלייליסט מותאם
        playlist_link = f"https://open.spotify.com/playlist/dummy_playlist_for_{country}_facecount_{face_count}"

        # החזרת התוצאה
        return jsonify({
            "message": "Face(s) detected successfully",
            "faceCount": face_count,
            "country": country,
            "playlist": playlist_link
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

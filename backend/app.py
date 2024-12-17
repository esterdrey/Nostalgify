import base64
import requests
from flask import Flask, render_template, send_from_directory, request, jsonify
import os
from io import BytesIO
from PIL import Image

# הגדרות ה-Azure Face API שלך
AZURE_ENDPOINT = "https://https://nostalgifyapp.cognitiveservices.azure.com/.cognitiveservices.azure.com/"
AZURE_API_KEY = "2iWX7sQ6mzHvGG18xGJQ2rUgbjInyQiQJ0o9pAB7BaO01c7tOxrAJQQJ99ALACYeBjFXJ3w3AAAKACOGc7zL"
FACE_API_URL = f"{AZURE_ENDPOINT}face/v1.0/detect"

# הגדרת Flask
app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')

@app.route('/')
def home():
    """הצגת עמוד הבית - index.html"""
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """שירות לקבצים סטטיים"""
    static_dir = os.path.join(app.root_path, '../frontend')
    return send_from_directory(static_dir, filename)

@app.route('/process', methods=['POST'])
def process_image():
    """עיבוד תמונה והערכת גיל באמצעות Azure Face API"""
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
        image = Image.open(BytesIO(image_binary))
        image.save("uploaded_image.png")

        # שליחת התמונה ל-Azure Face API
        headers = {
            "Ocp-Apim-Subscription-Key": AZURE_API_KEY,
            "Content-Type": "application/octet-stream"
        }
        params = {
            "returnFaceAttributes": "age"
        }
        response = requests.post(FACE_API_URL, headers=headers, params=params, data=image_binary)

        # בדיקת תגובה
        if response.status_code != 200:
            return jsonify({"error": f"Azure API Error: {response.text}"}), response.status_code

        # עיבוד התגובה מה-Azure
        faces = response.json()
        if not faces:
            return jsonify({"error": "No face detected in the image"}), 400

        # קבלת הגיל מהתוצאה
        age = faces[0]['faceAttributes']['age']

        # יצירת לינק לפלייליסט מותאם
        playlist_link = f"https://open.spotify.com/playlist/dummy_playlist_for_{country}_age_{int(age)}"

        # החזרת התוצאה
        return jsonify({
            "age": int(age),
            "country": country,
            "playlist": playlist_link
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

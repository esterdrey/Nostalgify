import base64
import requests
from flask import Flask, render_template, request, jsonify
from io import BytesIO
from PIL import Image
from deepface import DeepFace  # ספריית DeepFace

# הגדרת Flask
app = Flask(__name__)

@app.route('/')
def home():
    """הצגת עמוד הבית - index.html"""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    """עיבוד תמונה וזיהוי פנים וגילאים באמצעות DeepFace"""
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

        # שמירת התמונה לקובץ זמני
        temp_image_path = "uploaded_image.png"
        image = Image.open(BytesIO(image_binary))
        image.save(temp_image_path)

        # זיהוי גיל באמצעות DeepFace
        analysis = DeepFace.analyze(img_path=temp_image_path, actions=["age"], enforce_detection=False)
        age = analysis.get("age", "Unknown")

        # יצירת לינק לפלייליסט מותאם
        playlist_link = f"https://open.spotify.com/playlist/dummy_playlist_for_{country}_age_{age}"

        # החזרת התוצאה
        return jsonify({
            "message": "Face analyzed successfully",
            "age": age,
            "country": country,
            "playlist": playlist_link
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred : {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

import base64
import os
from flask import Flask, render_template, request, jsonify
from io import BytesIO
from PIL import Image
from deepface import DeepFace
from flask_cors import CORS

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
CORS(app)  # מוסיף תמיכה ב-CORS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    try:
        # קבלת נתוני JSON
        data = request.json
        if not data or 'image' not in data or 'country' not in data:
            return jsonify({"error": "Missing 'image' or 'country' in request"}), 400

        image_data = data['image']
        country = data['country']

        # המרת Base64 לתמונה
        try:
            header, encoded = image_data.split(",", 1)
            if not header.startswith("data:image/"):
                raise ValueError("Invalid image format")
            image_binary = base64.b64decode(encoded)
            image = Image.open(BytesIO(image_binary))
        except Exception as e:
            return jsonify({"error": f"Invalid image data: {str(e)}"}), 400

        # שמירת תמונה זמנית
        temp_image_path = "temp_image.jpg"
        image.save(temp_image_path)

        # שימוש ב-DeepFace עם PyTorch לניתוח גיל
        try:
            result = DeepFace.analyze(img_path=temp_image_path, actions=["age"])
            age = result.get("age", "Unknown")
        except Exception as analyze_error:
            return jsonify({"error": f"DeepFace analysis failed: {str(analyze_error)}"}), 500
        finally:
            # מחיקת קובץ זמני
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)

        # החזרת תוצאה
        playlist_link = f"https://open.spotify.com/playlist/dummy_playlist_for_{country}_facecount_{age}"
        return jsonify({"playlist": playlist_link, "age": age})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

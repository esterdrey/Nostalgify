import base64
import os
import numpy as np
from flask import Flask, render_template, send_from_directory, request, jsonify
from io import BytesIO
from PIL import Image
import insightface

# הגדרת Flask
app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')

# טוען את מודל InsightFace עם מודל קל יותר
def load_insightface_model():
    model = insightface.app.FaceAnalysis(name='buffalo_s')  # מודל קטן יותר
    model.prepare(ctx_id=-1)  # שימוש ב-CPU בלבד
    return model

# טוען את המודל בתחילת התוכנית
model = load_insightface_model()

# זיהוי גיל באמצעות InsightFace
def predict_age_with_insightface(image_path, model):
    img = Image.open(image_path).convert("RGB")
    img = np.array(img)

    # ניתוח הפנים בתמונה
    faces = model.get(img)
    if faces:
        return faces[0].age  # מחזיר את הגיל של הפנים הראשונות
    return "Unknown"

@app.route('/')
def home():
    """ מציג את עמוד הבית - index.html """
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    try:
        # קבלת הנתונים מה-Frontend
        data = request.json
        if not data or 'image' not in data or 'country' not in data:
            return jsonify({"error": "Missing 'image' or 'country' in request"}), 400

        image_data = data['image']
        country = data['country']

        # המרת התמונה לבינארי
        try:
            header, encoded = image_data.split(",", 1)
            image_binary = base64.b64decode(encoded)
            image = Image.open(BytesIO(image_binary)).convert("RGB")
        except Exception:
            return jsonify({"error": "Invalid image format"}), 400

        # שמירת התמונה לקובץ זמני
        temp_image_path = "temp_image.jpg"
        image.save(temp_image_path)

        # חיזוי גיל באמצעות InsightFace
        age = predict_age_with_insightface(temp_image_path, model)
        os.remove(temp_image_path)

        # ניקוי זיכרון
        del image, image_binary

        # יצירת לינק מותאם
        playlist_link = f"https://open.spotify.com/playlist/dummy_playlist_for_{country}_facecount_{age}"
        return jsonify({"playlist": playlist_link, "age": age})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/frontend/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('../frontend', filename)

@app.after_request
def add_header(response):
    """ מונע שמירה של קבצים במטמון """
    response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

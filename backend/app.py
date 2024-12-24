from flask import Flask, render_template, jsonify, request
import base64
from io import BytesIO
from PIL import Image
from deepface import DeepFace

# הגדרת Flask עם הנתיבים הנוכחיים שלך
app = Flask(__name__, template_folder='../frontend', static_folder='../frontend')

@app.route('/')
def home():
    """הצגת עמוד הבית"""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    """עיבוד תמונה וזיהוי גיל"""
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

        # ניתוח תמונה עם DeepFace
        analysis = DeepFace.analyze(img_path=temp_image_path, actions=["age"], enforce_detection=False)
        age = analysis.get("age", "Unknown")

        # יצירת קישור לפלייליסט
        playlist_link = f"https://open.spotify.com/playlist/dummy_playlist_for_{country}_age_{age}"

        # החזרת תשובה ל-Frontend
        return jsonify({
            "message": "Face analyzed successfully",
            "age": age,
            "country": country,
            "playlist": playlist_link
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

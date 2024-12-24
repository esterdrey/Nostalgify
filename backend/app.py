from flask import Flask, render_template, jsonify, request
import base64
from io import BytesIO
from PIL import Image
from deepface import DeepFace

# הגדרת Flask עם הנתיבים למבנה הקיים שלך
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
            print("ERROR: Missing 'image' or 'country' in request")
            return jsonify({"error": "Missing 'image' or 'country' in request"}), 400

        image_data = data['image']
        country = data['country']

        # המרת התמונה לבינארי
        try:
            header, encoded = image_data.split(",", 1)
            image_binary = base64.b64decode(encoded)
        except Exception as e:
            print(f"ERROR: Failed to decode image - {str(e)}")
            return jsonify({"error": "Failed to decode image"}), 400

        # שמירת התמונה לקובץ זמני
        temp_image_path = "uploaded_image.png"
        try:
            image = Image.open(BytesIO(image_binary))
            image.save(temp_image_path)
        except Exception as e:
            print(f"ERROR: Failed to save image - {str(e)}")
            return jsonify({"error": "Failed to save image"}), 500

        # ניתוח תמונה עם DeepFace
        try:
            analysis = DeepFace.analyze(img_path=temp_image_path, actions=["age"], enforce_detection=False)
            age = analysis.get("age", "Unknown")
        except Exception as e:
            print(f"ERROR: DeepFace analysis failed - {str(e)}")
            return jsonify({"error": "DeepFace analysis failed"}), 500

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
        print(f"ERROR: An unexpected error occurred - {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)

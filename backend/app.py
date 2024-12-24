from flask import Flask, render_template, jsonify, request
import base64
from io import BytesIO
from PIL import Image
from deepface import DeepFace
import os

# הגדרת Flask
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
            return jsonify({"error": "Missing 'image' or 'country'"}), 400

        image_data = data['image']
        header, encoded = image_data.split(",", 1)
        image_binary = base64.b64decode(encoded)

        # שמירת התמונה לקובץ זמני
        temp_image_path = "uploaded_image.png"
        image = Image.open(BytesIO(image_binary))
        image.save(temp_image_path)

        # ניתוח תמונה עם DeepFace
        analysis = DeepFace.analyze(img_path=temp_image_path, actions=["age"], enforce_detection=False)
        age = analysis.get("age", "Unknown")

        # החזרת תשובה
        return jsonify({
            "message": "Face analyzed successfully",
            "age": age
        })

    except Exception as e:
        print(f"ERROR: {str(e)}")  # לוג לשרת
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render דורש להשתמש במשתנה PORT
    app.run(debug=True, host="0.0.0.0", port=port)

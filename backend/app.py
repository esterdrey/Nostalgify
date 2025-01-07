import base64
import os
import requests
from flask import Flask, render_template, send_from_directory, request, jsonify
import os
from io import BytesIO
from PIL import Image
from deepface import DeepFace
from deepface.commons import functions
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
functions.backend = "torch"


# הגדרת Flask
app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')

@app.route('/')
def home():
    """ הצגת עמוד הבית - index.html"""
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

        # והפרדת HEADER המרת התמונה לבינארי
        header, encoded = image_data.split(",", 1)
        image_binary = base64.b64decode(encoded)

        #יצירת אובייקט תמונה 
        image = Image.open(BytesIO(image_binary))

        # שמירת התמונה לקובץ זמני)
        temp_image_path = "temp_image.jpg"
        image.save(temp_image_path)

        # ניתוח גיל 
        result = DeepFace.analyze(img_path=temp_image_path, actions=["age"])
        age = result.get("age", "Unknown")

        # ניקוי קובץ זמני
        os.remove(temp_image_path)

        # החזרת הגיל כמספר בלבד
        #return str(age)
   

        # יצירת לינק לפלייליסט מותאם
        playlist_link = f"https://open.spotify.com/playlist/dummy_playlist_for_{country}_facecount_{age}"
        return jsonify({"playlist": playlist_link, "age": age})

  
    except Exception as e:
        return jsonify({"error": f"An error occurred : {str(e)}"}), 500

@app.route('/frontend/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('../frontend', filename)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == '__main__':
    # app.run(debug=True, host="0.0.0.0", port=5000) 
    port = int(os.environ.get("PORT", 5000)) 
    app.run(debug=True, host="0.0.0.0", port=port)
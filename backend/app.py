import base64
import os
import torch
import requests
from torchvision import transforms
from flask import Flask, render_template, send_from_directory, request, jsonify
from io import BytesIO
from PIL import Image

# הגדרת Flask
app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')

import requests

def predict_age(image_path):
    url = "https://api.deepai.org/api/demographic-recognition"
    try:
        with open(image_path, 'rb') as image_file:
            response = requests.post(
                url,
                files={'image': image_file},
                headers={'api-key': '6e1b8fec-b405-41c6-813e-6a820e93f9f5'}
            )
        result = response.json()
        if 'output' in result and 'faces' in result['output'] and len(result['output']['faces']) > 0:
            age = result['output']['faces'][0]['age']
            return age
        else:
            return "Error: No faces detected."
    except Exception as e:
        return f"Error: {str(e)}"



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
        age = predict_age(temp_image_path)

        # ניקוי קובץ זמני
        os.remove(temp_image_path)

        # החזרת הגיל כמספר בלבד
        #return str(age)
   

        # יצירת לינק לפלייליסט מותאם
        playlist_link = f"https://open.spotify.com/playlist/dummy_playlist_for_{country}_facecount_{age}"
        return jsonify({"playlist": playlist_link, "age": age})

  
    except Exception as e:
        return jsonify({"error": f"An error occurred : {str(e)}"}), 500

@app.route('/models/<path:filename>')
def serve_models(filename):
    return send_from_directory('models', filename)

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
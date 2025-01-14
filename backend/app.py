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


@app.route('/')
def home():
    """ הצגת עמוד הבית - index.html"""
    return render_template('index.html')

# הגשת מודלים כסטטיים
@app.route('/models/<path:filename>')
def serve_models(filename):
    return send_from_directory('models', filename)
# הגשת קבצים סטטיים
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend', filename)

@app.route('/process', methods=['POST'])
def process_image():
 
    try:
        # קבלת הנתונים מה-Frontend
        data = request.json
        age = data.get('age')
        country = data.get('country')

        if not age or not country:
            return jsonify({"error": "Missing age or country in request"}), 400


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
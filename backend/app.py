import base64
from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_cors import CORS  # מאפשר CORS בין דומיינים שונים
import os
from io import BytesIO
from PIL import Image

# הגדרת ה-App עם Flask
app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')
CORS(app)  # מאפשר CORS

@app.route('/')
def home():
    return render_template('index.html')  # מציג את index.html

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, '../frontend/static'), filename)

@app.route('/process', methods=['POST'])
def process_image():
    try:
        # קבלת המידע מה-Frontend
        data = request.json
        if 'image' not in data or 'country' not in data:
            raise ValueError("Missing 'image' or 'country' in the request.")

        image_data = data['image']  # התמונה בפורמט base64
        country = data['country']

        # המרת התמונה לבינארי
        header, encoded = image_data.split(",", 1)
        image_binary = base64.b64decode(encoded)

        # טעינת התמונה לשמירה או עיבוד
        image = Image.open(BytesIO(image_binary))
        image.save("uploaded_image.png")  # שמירת התמונה לבדיקה

        # סימולציה לקריאת Azure Face API או חישוב הגיל
        age = 25  # כאן ניתן להוסיף קריאה אמיתית ל-Azure API או אלגוריתם מתאים

        # יצירת לינק לפלייליסט מבוסס מדינה וגיל
        playlist_link = f"https://open.spotify.com/playlist/dummy_playlist_for_{country}_age_{age}"

        # שליחת התוצאה חזרה ל-Frontend
        return jsonify({"age": age, "country": country, "playlist": playlist_link})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

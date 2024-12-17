import base64
from flask import Flask, render_template, send_from_directory, request, jsonify
import os
from io import BytesIO
from PIL import Image

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')

@app.route('/')
def home():
    return render_template('index.html')  # מציג את index.html

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, '../frontend'), filename)

@app.route('/process', methods=['POST'])
def process_image():
    try:
        # קבלת המידע מה-Frontend
        data = request.json
        image_data = data['image']  # התמונה בפורמט base64
        country = data['country']

        # המרת התמונה לבינארי
        header, encoded = image_data.split(",", 1)
        image_binary = base64.b64decode(encoded)

        # שמירת התמונה כקובץ זמני (אם נדרש)
        image = Image.open(BytesIO(image_binary))
        image.save("uploaded_image.png")  # שמירת התמונה לבדיקה

        # כאן תבצעי את קריאת ה-Azure Face API
        # במקום ה-Azure אמיתי, תחזיר תוצאה דמוית גיל
        age = 25  # ערך דמיוני לדוגמה

        # יצירת לינק לפלייליסט (אפשר לשלב לוגיקה לפי גיל ומדינה)
        playlist_link = f"https://open.spotify.com/playlist/dummy_playlist_for_{country}_age_{age}"

        # שליחת התוצאה חזרה ל-Frontend
        return jsonify({"age": age, "country": country, "playlist": playlist_link})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

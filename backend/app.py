import base64
from flask import Flask, render_template, send_from_directory, request, jsonify
import os
from io import BytesIO
from PIL import Image

# הגדרת תיקיות סטטיות ותבניות בצורה תקינה
app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')

@app.route('/')
def home():
    """הצגת עמוד הבית - index.html"""
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """שירות לקבצים סטטיים"""
    static_dir = os.path.join(app.root_path, '../frontend')
    return send_from_directory(static_dir, filename)

@app.route('/process', methods=['POST'])
def process_image():
    """עיבוד התמונה שנשלחת מה-Frontend"""
    try:
        # קבלת המידע מה-Frontend
        data = request.json
        if not data or 'image' not in data or 'country' not in data:
            return jsonify({"error": "Missing 'image' or 'country' in request"}), 400

        image_data = data['image']
        country = data['country']

        # המרת התמונה מבסיס64 לבינארי
        header, encoded = image_data.split(",", 1)
        image_binary = base64.b64decode(encoded)

        # שמירת התמונה כקובץ זמני לבדיקה
        temp_image_path = "uploaded_image.png"
        image = Image.open(BytesIO(image_binary))
        image.save(temp_image_path)

        # דימוי של קריאת Azure Face API (לצורך בדיקה)
        age = 25  # ערך דמיוני לשם דוגמה

        # יצירת לינק לפלייליסט מותאם
        playlist_link = f"https://open.spotify.com/playlist/dummy_playlist_for_{country}_age_{age}"

        # שליחת התוצאה חזרה ל-Frontend
        return jsonify({
            "age": age,
            "country": country,
            "playlist": playlist_link
        })

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # הפעלה מקומית של השרת
    app.run(debug=True, host="0.0.0.0", port=5000)

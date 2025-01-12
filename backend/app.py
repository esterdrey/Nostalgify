import base64
import os
import torch
from torchvision import transforms
from flask import Flask, render_template, send_from_directory, request, jsonify
from io import BytesIO
from PIL import Image, UnidentifiedImageError

# הגדרת Flask
app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend')

def predict_age(image_path):
    model = torch.hub.load('yu4u/age-gender-estimation', 'age_model', pretrained=True)
    model.eval()

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    image = Image.open(image_path).convert("RGB")
    image_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(image_tensor)
        predicted_age = output.argmax().item()

    return predicted_age


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

        # המרת התמונה לבינארי
        try:
            header, encoded = image_data.split(",", 1)
            image_binary = base64.b64decode(encoded)
            image = Image.open(BytesIO(image_binary))
        except UnidentifiedImageError:
            return jsonify({"error": "Invalid image format"}), 400

        # שמירת התמונה לקובץ זמני
        temp_image_path = "temp_image.jpg"
        image.save(temp_image_path)

        # ניתוח גיל
        age = predict_age(temp_image_path)

        # ניקוי קובץ זמני
        os.remove(temp_image_path)

        # יצירת לינק לפלייליסט מותאם
        playlist_link = f"https://open.spotify.com/playlist/dummy_playlist_for_{country}_facecount_{age}"
        return jsonify({"playlist": playlist_link, "age": age})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/frontend/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('../frontend/static', filename)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

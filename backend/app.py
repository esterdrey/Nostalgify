import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Azure Face API credentials
API_KEY = "YOUR_API_KEY"  # הכניסי את ה-Primary Key
ENDPOINT = "YOUR_ENDPOINT_URL"  # הכניסי את ה-Endpoint URL

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyzes an image uploaded by the user and detects the age of the face.
    Also receives the user's childhood country.
    """
    # קבלת התמונה והמדינה
    file = request.files.get('image')
    country = request.form.get('country', 'Unknown')

    if not file:
        return jsonify({"error": "No image provided"}), 400

    # הכנת הכותרות לבקשה ל-Azure Face API
    headers = {
        'Ocp-Apim-Subscription-Key': API_KEY,
        'Content-Type': 'application/octet-stream'
    }
    params = {
        'returnFaceAttributes': 'age'
    }

    # שליחת התמונה ל-Azure Face API
    response = requests.post(f"{ENDPOINT}/face/v1.0/detect", headers=headers, params=params, data=file.read())
    
    # בדיקת שגיאות בתגובה מה-API
    if response.status_code != 200:
        return jsonify({"error": f"Error with Azure API: {response.text}"}), response.status_code

    # עיבוד התוצאה מה-API
    result = response.json()
    if not result:
        return jsonify({"error": "No face detected"}), 400

    # הוצאת הגיל מהתוצאה
    age = result[0]['faceAttributes']['age']

    # החזרת תוצאה ל-Frontend
    return jsonify({"age": age, "country": country, "message": "Analysis successful"})

if __name__ == '__main__':
    app.run(debug=True)

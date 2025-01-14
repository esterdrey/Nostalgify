from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='frontend')

# דף הבית
@app.route('/')
def home():
    return send_from_directory('frontend', 'index.html')

# הגשת קבצים סטטיים (JS, CSS וכו')
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('frontend', filename)

# מסלול לזיהוי פנים
@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['file']
    file.save('uploaded_image.jpg')

    # כאן מתבצע זיהוי הפנים
    import cv2
    img = cv2.imread('uploaded_image.jpg')
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    return jsonify({"faces_detected": len(faces)})

if __name__ == '__main__':
    app.run()

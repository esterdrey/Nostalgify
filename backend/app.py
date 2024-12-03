from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files['image']
    if not file:
        return jsonify({"error": "No image provided"}), 400

    # Mock s גיל
    return jsonify({"age": 25, "message": "Analysis uccessful"})

if __name__ == '__main__':
    app.run(debug=True)
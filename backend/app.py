@app.route('/process', methods=['POST'])
def process_image():
    try:
        logging.debug("Received request at /process")
        data = request.json
        if not data or 'image' not in data or 'country' not in data:
            logging.error("Missing 'image' or 'country' in request")
            return jsonify({"error": "Missing 'image' or 'country' in request"}), 400

        image_data = data['image']
        country = data['country']
        logging.debug(f"Received data: country={country}")

        # שמירה זמנית של התמונה
        header, encoded = image_data.split(",", 1)
        image_binary = base64.b64decode(encoded)
        temp_image_path = "temp_image.jpg"

        with open(temp_image_path, "wb") as f:
            f.write(image_binary)
        logging.debug(f"Image saved temporarily at {temp_image_path}")

        # חיזוי גיל
        age = predict_age_with_insightface(temp_image_path)
        os.remove(temp_image_path)
        logging.debug(f"Predicted age: {age}")

        # יצירת לינק מותאם
        playlist_link = f"https://open.spotify.com/playlist/dummy_playlist_for_{country}_facecount_{age}"
        logging.debug(f"Generated playlist link: {playlist_link}")

        return jsonify({"playlist": playlist_link, "age": age})

    except Exception as e:
        logging.exception("An error occurred in /process")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

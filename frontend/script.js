document.addEventListener('DOMContentLoaded', () => {
    const uploadInput = document.getElementById('upload'); 
    const submitButton = document.getElementById('submit');
    const resultDiv = document.getElementById('result');
    const preview = document.getElementById('preview');

    // אתחול Mediapipe Face Detection
    const faceDetector = new FaceDetection.FaceDetector({
        locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_detection/${file}`
    });

    faceDetector.setOptions({
        model: 'short', // או 'full' אם תרצה דיוק גבוה יותר
        minDetectionConfidence: 0.5
    });

    // העלאת תמונה
    uploadInput.addEventListener('change', async (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = async (e) => {
                preview.src = e.target.result;
                preview.style.display = 'block';

                const img = new Image();
                img.src = e.target.result;
                img.onload = async () => {
                    const detections = await faceDetector.send({ image: img });
                    if (detections.detections.length > 0) {
                        const age = estimateAgeFromFace(detections.detections[0]);
                        resultDiv.innerHTML = `<p>Your estimated age: ${age} years old</p>`;
                    } else {
                        alert('No face detected.');
                    }
                };
            };
            reader.readAsDataURL(file);
        }
    });

    // פונקציה לדוגמה כדי להעריך גיל (היא כרגע מדמה גיל, צריך לשפר את המודל)
    function estimateAgeFromFace(face) {
        // כאן תוכל להוסיף לוגיקה מתקדמת יותר עם TensorFlow.js
        return Math.floor(Math.random() * 30) + 20; // גיל רנדומלי בין 20 ל-50
    }
});

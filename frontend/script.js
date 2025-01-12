// טוען את המודלים ברגע שהדף נטען
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // טוענים את המודלים מהתיקייה /models
        await faceapi.nets.ssdMobilenetv1.loadFromUri('/static/models');
        await faceapi.nets.ageGenderNet.loadFromUri('/static/models');

        console.log("Models loaded successfully.");
    } catch (error) {
        console.error("Error loading models:", error);
        document.getElementById('result').innerHTML = `<p>Error: Unable to load models.</p>`;
        return;
    }

    // הגדרת משתנים עבור אלמנטים ב-HTML
    const uploadInput = document.getElementById('upload');
    const resultDiv = document.getElementById('result');
    const preview = document.getElementById('preview');

    // אירוע של העלאת תמונה
    uploadInput.addEventListener('change', async (event) => {
        const file = event.target.files[0];
        if (file) {
            // הצגת התמונה בתצוגה מקדימה
            const image = await faceapi.bufferToImage(file);
            preview.src = URL.createObjectURL(file);
            preview.style.display = 'block';

            // ניתוח התמונה לזיהוי גיל ומגדר
            const detections = await faceapi.detectSingleFace(image).withAgeAndGender();
            if (detections) {
                const age = Math.round(detections.age);
                const gender = detections.gender;
                resultDiv.innerHTML = `
                    <p>Your playlist is ready!</p>
                    <p>Your age is: ${age}</p>
                    <p>Your gender is: ${gender}</p>
                `;
            } else {
                resultDiv.innerHTML = `<p>Error: No face detected. Please upload a clear image.</p>`;
            }
        }
    });
});

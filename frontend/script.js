document.addEventListener('DOMContentLoaded', async () => {
    // טוענים את המודל
    await faceapi.nets.ageGenderNet.loadFromUri('/models');
    await faceapi.nets.ssdMobilenetv1.loadFromUri('/models');

    const uploadInput = document.getElementById('upload'); 
    const submitButton = document.getElementById('submit');
    const resultDiv = document.getElementById('result');
    const preview = document.getElementById('preview');
    let imageData = null;

    uploadInput.addEventListener('change', async (event) => {
        const file = event.target.files[0];
        if (file) {
            const image = await faceapi.bufferToImage(file);
            preview.src = URL.createObjectURL(file);
            preview.style.display = 'block';

            // ניתוח התמונה
            const detections = await faceapi.detectSingleFace(image).withAgeAndGender();
            if (detections) {
                const age = Math.round(detections.age);
                resultDiv.innerHTML = `<p>Your playlist is ready!<br>Your age is: ${age}</p>`;
            } else {
                resultDiv.innerHTML = `<p>Error: Unable to detect face.</p>`;
            }
        }
    });
});

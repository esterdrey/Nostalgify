async function loadModels() {
    await faceapi.nets.ssdMobilenetv1.loadFromUri('/models');
    await faceapi.nets.ageGenderNet.loadFromUri('/models');
    await faceapi.nets.faceLandmark68Net.loadFromUri('/models');
    console.log("Models loaded successfully!");
}

document.addEventListener('DOMContentLoaded', async () => {

    await loadModels();
    console.log("Ready to detect faces!");
    const uploadInput = document.getElementById('upload'); 
    const submitButton = document.getElementById('submit');
    const resultDiv = document.getElementById('result');
    const preview = document.getElementById('preview');
    let imageData = null;

    // העלאת תמונה קיימת
    uploadInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imageData = e.target.result; // שמירת נתוני התמונה
                preview.src = e.target.result; // הצגת התמונה
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });

        // ניתוח התמונה לגיל
        uploadInput.addEventListener('change', async (event) => {
            const file = event.target.files[0];
            const img = await faceapi.bufferToImage(file);
    
            const detection = await faceapi.detectSingleFace(img).withAgeAndGender();
            if (detection) {
                detectedAge = Math.round(detection.age);
                resultDiv.innerHTML = `<p>Detected Age: ${detectedAge}</p>`;
            } else {
                resultDiv.innerHTML = `<p>No face detected!</p>`;
            }
        });

     // שליחת הגיל והמדינה לשרת
    submitButton.addEventListener('click', () => {
        const country = document.getElementById('country').value;

        if (!detectedAge) {
            alert('Please upload an image and wait for age detection.');
            return;
        }

        if (!country) {
            alert('Please enter your country.');
            return;
        }

        fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ age: detectedAge, country })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`Error: ${data.error}`);
            } else {
                resultDiv.innerHTML = `
                <p>Your playlist is ready: <a href="${data.playlist}" target="_blank">Open Playlist</a></p>
                `;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });
});
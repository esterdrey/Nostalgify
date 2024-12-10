const cameraPreview = document.getElementById('camera'); // התצוגה של המצלמה
const captureButton = document.getElementById('capture'); // כפתור צילום
const uploadInput = document.getElementById('upload'); // כפתור העלאת תמונה
const submitButton = document.getElementById('submit'); // כפתור שליחה

let imageData = null; // כאן נשמור את התמונה המצולמת או המועלת

// גישה למצלמה
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        cameraPreview.srcObject = stream;
    })
    .catch(error => {
        console.error("Error accessing camera: ", error);
    });

// צילום תמונה
captureButton.addEventListener('click', () => {
    const canvas = document.createElement('canvas');
    canvas.width = cameraPreview.videoWidth;
    canvas.height = cameraPreview.videoHeight;
    canvas.getContext('2d').drawImage(cameraPreview, 0, 0);
    imageData = canvas.toDataURL('image/png');
    alert('Image captured successfully!');
});

// העלאת תמונה קיימת
uploadInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = () => {
        imageData = reader.result;
        alert('Image uploaded successfully!');
    };
    reader.readAsDataURL(file);
});

// שליחת נתונים לשרת
submitButton.addEventListener('click', () => {
    const country = document.getElementById('country').value;
    if (!imageData) {
        alert('Please capture or upload an image.');
        return;
    }
    fetch('/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageData, country })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(`Error: ${data.error}`);
        } else {
            alert(`Playlist: ${data.playlist}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
});

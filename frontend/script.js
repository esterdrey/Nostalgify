const video = document.getElementById('camera');
const captureButton = document.getElementById('capture');
const uploadInput = document.getElementById('upload');
const submitButton = document.getElementById('submit');

let imageData = null;

// גישה למצלמה
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    });

// צילום תמונה
captureButton.addEventListener('click', () => {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    imageData = canvas.toDataURL('image/png');
});

// העלאת תמונה קיימת
uploadInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = () => {
        imageData = reader.result;
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
    fetch('http://127.0.0.1:5000/process', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageData, country })
    })
    .then(response => response.json())
    .then(data => {
        alert(`Playlist: ${data.playlist}`);
    });
});
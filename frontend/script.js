document.addEventListener('DOMContentLoaded', () => {
    const uploadInput = document.getElementById('upload');
    const submitButton = document.getElementById('submit');
    const resultDiv = document.getElementById('result');

    let imageData = null;

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
        if (!country) {
            alert('Please enter your childhood country.');
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
                resultDiv.innerHTML = `<p>Your playlist is ready: <a href="${data.playlist}" target="_blank">Open Playlist</a></p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });
});

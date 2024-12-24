document.addEventListener('DOMContentLoaded', () => {
    const uploadInput = document.getElementById('upload');
    const submitButton = document.getElementById('submit');
    const preview = document.getElementById('preview');
    const resultDiv = document.getElementById('result');
    let imageData = null;

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

    submitButton.addEventListener('click', () => {
        const country = document.getElementById('country').value;
        if (!imageData) {
            alert('Please upload an image.');
            return;
        }
        if (!country) {
            alert('Please enter your childhood country.');
            return;
        }
        fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: imageData, country }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert(`Error: ${data.error}`);
            } else {
                resultDiv.innerHTML = `<p>Age: ${data.age}</p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        });
    });
});

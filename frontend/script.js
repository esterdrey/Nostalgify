document.addEventListener('DOMContentLoaded', () => {
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

    // שליחת נתונים לשרת
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
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData, country })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(`Error: ${data.error}`);
            } else {
                // הצגת הגיל לצד הפלייליסט
                const ages = data.ages.join(", ");
                resultDiv.innerHTML = `
                    <p>Detected age(s): ${ages}</p>
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

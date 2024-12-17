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
            // הצגת התוצאה במסך המשתמש
            resultDiv.innerHTML = `
                <p>Detected ${data.faceCount} face(s).</p>
                <p>Your playlist: <a href="${data.playlist}" target="_blank">Open Playlist</a></p>
            `;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
});

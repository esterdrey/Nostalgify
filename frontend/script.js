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
            resultDiv.innerHTML = `<p>Your playlist is ready: <a href="${data.playlist}" target="_blank">Open Playlist</a></p>`;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
});

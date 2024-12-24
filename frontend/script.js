document.getElementById('submit').addEventListener('click', async function () {
    const fileInput = document.getElementById('fileInput');
    const countryInput = document.getElementById('countryInput');
    const resultDiv = document.getElementById('result');
    const country = countryInput.value;

    if (!fileInput.files[0]) {
        alert('Please choose a file!');
        return;
    }

    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = async function () {
        const imageData = reader.result;

        try {
            const response = await fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ image: imageData, country }),
            });

            console.log('Response status:', response.status);

            if (!response.ok) {
                throw new Error('Server error: ' + response.status);
            }

            const data = await response.json();
            console.log('Response data:', data);

            if (data.error) {
                alert(`Error: ${data.error}`);
            } else {
                resultDiv.innerHTML = `<p>Your playlist is ready: <a href="${data.playlist}" target="_blank">Open Playlist</a></p>`;
            }
        } catch (error) {
            console.error('Fetch error:', error);
            alert('An error occurred. Please try again.');
        }
    };

    reader.readAsDataURL(file);
});

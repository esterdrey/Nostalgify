const uploadInput = document.getElementById('upload');
const submitButton = document.getElementById('submit');
const resultDiv = document.getElementById('result');

uploadInput.addEventListener('change', () => {
    const file = uploadInput.files[0];
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('/detect', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            resultDiv.innerHTML = `<p>Faces detected: ${data.faces_detected}</p>`;
        })
        .catch(error => {
            console.error('Error:', error);
            resultDiv.innerHTML = `<p>Error: ${error}</p>`;
        });
    }
});

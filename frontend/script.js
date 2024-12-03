const form = document.querySelector('#image-form');
form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const fileInput = document.querySelector('#file-input');
    const country = document.querySelector('#country').value;
    const formData = new FormData();
    formData.append('image', fileInput.files[0]);
    formData.append('country', country);

    try {
        const response = await fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        document.querySelector('#result').textContent = `Age: ${data.age}, Country: ${data.country}`;
    } catch (error) {
        document.querySelector('#result').textContent = 'Error analyzing image.';
    }
});
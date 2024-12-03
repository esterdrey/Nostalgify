const form = document.querySelector('#image-form');
form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const fileInput = document.querySelector('#file-input');
    const result = document.querySelector('#result');

    const formData = new FormData();
    formData.append('image', fileInput.files[0]);

    try {
        const response = await fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        result.textContent = `Estimated Age: ${data.age}`;
    } catch (error) {
        result.textContent = 'Error analyzing image';
    }
});

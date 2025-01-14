document.addEventListener('DOMContentLoaded', async () => {
    const uploadInput = document.getElementById('upload');
    const preview = document.getElementById('preview');
    const submitButton = document.getElementById('submit');
    const resultDiv = document.getElementById('result');
    const countryInput = document.getElementById('country');

    // טעינת Human.js
    const human = new Human.Human();
    await human.load();

    // תצוגה מקדימה של התמונה
    uploadInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                preview.src = e.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });

    // חישוב הגיל מהתמונה והצגת הפלייליסט
    submitButton.addEventListener('click', async () => {
        const country = countryInput.value.trim().toLowerCase();

        if (!preview.src) {
            alert('Please upload an image.');
            return;
        }

        // זיהוי הגיל מהתמונה באמצעות Human.js
        const img = new Image();
        img.src = preview.src;
        await img.decode();

        const result = await human.detect(img);

        if (result.face.length === 0) {
            alert('No face detected. Please upload a clear image.');
            return;
        }

        const age = Math.round(result.face[0].age);
        const decade = Math.floor(age / 10) * 10;

        // חישוב הפלייליסט
        const key = `${country}_${decade}s`;
        const playlistLink = playlists[key] || "https://open.spotify.com/playlist/37i9dQZF1DX4UtSsGT1Sbe";

        // הצגת התוצאה
        resultDiv.innerHTML = `
            <p>Your playlist: <a href="${playlistLink}" target="_blank">Open Playlist</a></p>
            <p>Age detected: ${age}</p>
        `;
    });
});

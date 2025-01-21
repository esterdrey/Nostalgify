document.addEventListener('DOMContentLoaded', async () => {
    const uploadInput = document.getElementById('upload');
    const preview = document.getElementById('preview');
    const submitButton = document.getElementById('submit');
    const resultDiv = document.getElementById('result');
    const countryInput = document.getElementById('country');

    // טעינת Human.js עם הגדרה לטעינת המודלים מ-GitHub
    const human = new Human.Human({
        modelBasePath: 'https://raw.githubusercontent.com/vladmandic/human/main/models', // נתיב המודלים
        backend: 'webgl', // שימוש ב-webgl במקום webgpu
    });
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

        // יצירת פלייליסט באמצעות Spotify API
        try {
            const playlistLink = await getSpotifyPlaylist(country, decade);
            resultDiv.innerHTML = `
                <p>Your playlist: <a href="${playlistLink}" target="_blank">Open Playlist</a></p>
                <p>Age detected: ${age}</p>
            `;
        } catch (error) {
            console.error('Error fetching playlist:', error);
            resultDiv.innerHTML = `<p>Failed to fetch playlist. Please try again later.</p>`;
        }
    });
});

// פונקציה ליצירת בקשת פלייליסט ל-Spotify API
async function getSpotifyPlaylist(country, decade) {
    const SPOTIFY_TOKEN = 'YOUR_SPOTIFY_ACCESS_TOKEN'; // הכנס את ה-Access Token שלך כאן

    // יצירת שאילתה על סמך עשור ומדינה
    const query = `${country} ${decade}s`;
    const url = `https://api.spotify.com/v1/search?q=${encodeURIComponent(query)}&type=playlist&limit=1`;

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${SPOTIFY_TOKEN}`
        }
    });

    if (!response.ok) {
        throw new Error('Spotify API error: ' + response.status);
    }

    const data = await response.json();

    if (data.playlists.items.length === 0) {
        throw new Error('No playlists found for query: ' + query);
    }

    return data.playlists.items[0].external_urls.spotify; // קישור לפלייליסט
}

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

    // פונקציה לקבלת Access Token מ-Spotify
    async function getSpotifyAccessToken() {
        const clientId = 'YOUR_CLIENT_ID'; // הכניסי כאן את ה-Client ID שלך
        const clientSecret = 'YOUR_CLIENT_SECRET'; // הכניסי כאן את ה-Client Secret שלך

        const response = await fetch('https://accounts.spotify.com/api/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic ' + btoa(clientId + ':' + clientSecret)
            },
            body: 'grant_type=client_credentials'
        });

        const data = await response.json();
        return data.access_token; // מחזיר את ה-Access Token
    }

    // פונקציה לחיפוש פלייליסטים ב-Spotify
    async function searchSpotifyPlaylists(query) {
        const accessToken = await getSpotifyAccessToken();

        const response = await fetch(`https://api.spotify.com/v1/search?q=${encodeURIComponent(query)}&type=playlist`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        const data = await response.json();
        return data.playlists.items; // מחזיר את הפלייליסטים
    }

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

        // יצירת מחרוזת החיפוש ל-Spotify
        const query = `${country} ${decade}s hits`;

        // חיפוש פלייליסטים ב-Spotify
        const playlists = await searchSpotifyPlaylists(query);

        // הצגת הפלייליסט הראשון בתוצאה
        if (playlists.length > 0) {
            const playlist = playlists[0]; // הפלייליסט הראשון
            resultDiv.innerHTML = `
                <p>Your playlist: <a href="${playlist.external_urls.spotify}" target="_blank">${playlist.name}</a></p>
                <p>Age detected: ${age}</p>
            `;
        } else {
            resultDiv.innerHTML = '<p>No playlists found!</p>';
        }
    });
});
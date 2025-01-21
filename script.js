document.addEventListener('DOMContentLoaded', async () => {
    const uploadInput = document.getElementById('upload');
    const preview = document.getElementById('preview');
    const submitButton = document.getElementById('submit');
    const resultDiv = document.getElementById('result');
    const countryInput = document.getElementById('country');

    // טעינת Human.js עם הגדרה לטעינת המודלים מ-GitHub
    const human = new Human.Human({
        modelBasePath: 'https://raw.githubusercontent.com/vladmandic/human/main/models',
        backend: 'webgl',
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

    // קבלת Access Token מ-Spotify
    async function getAccessToken(9e5becb2c8764dada9b60a8f3b3855c6, b0de34c77ea64efa9cbf661f08b495e6) {
        const url = 'https://accounts.spotify.com/api/token';
        const credentials = btoa(`${clientId}:${clientSecret}`); // קידוד Base64

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Authorization': `Basic ${credentials}`,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'grant_type=client_credentials',
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch access token: ${response.status}`);
        }

        const data = await response.json();
        return data.access_token; // מחזיר את ה-Access Token
    }

    // חיפוש פלייליסט ציבורי לפי שאילתה
    async function searchPublicPlaylist(query, accessToken) {
        const url = `https://api.spotify.com/v1/search?q=${encodeURIComponent(query)}&type=playlist&limit=1`;

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
            },
        });

        if (!response.ok) {
            throw new Error(`Spotify API error: ${response.status}`);
        }

        const data = await response.json();

        if (data.playlists.items.length === 0) {
            throw new Error(`No playlists found for query: ${query}`);
        }

        return data.playlists.items[0].external_urls.spotify; // מחזיר קישור לפלייליסט
    }

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

        // קבלת Access Token ובקשה ל-Spotify API
        const clientId = 'YOUR_CLIENT_ID'; // הכנס את ה-Client ID שלך
        const clientSecret = 'YOUR_CLIENT_SECRET'; // הכנס את ה-Client Secret שלך

        try {
            const accessToken = await getAccessToken(clientId, clientSecret);

            // יצירת שאילתה על סמך המדינה והעשור
            const query = `${country} ${decade}s`;
            const playlistLink = await searchPublicPlaylist(query, accessToken);

            // הצגת התוצאה
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
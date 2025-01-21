document.addEventListener('DOMContentLoaded', async () => {
    const uploadInput = document.getElementById('upload');
    const preview = document.getElementById('preview');
    const submitButton = document.getElementById('submit');
    const resultDiv = document.getElementById('result');
    const countryInput = document.getElementById('country');

    const human = new Human.Human({
        modelBasePath: 'https://raw.githubusercontent.com/vladmandic/human/main/models',
        backend: 'webgl',
    });
    await human.load();

    // פונקציה לקבלת Access Token מ-Spotify
    async function getSpotifyAccessToken() {
        const clientId = '9e5becb2c8764dada9b60a8f3b3855c6';
        const clientSecret = 'b0de34c77ea64efa9cbf661f08b495e6';

        const response = await fetch('https://accounts.spotify.com/api/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic ' + btoa(clientId + ':' + clientSecret)
            },
            body: 'grant_type=client_credentials'
        });

        const data = await response.json();
        return data.access_token;
    }

    // פונקציה לחיפוש פלייליסטים ב-Spotify
    async function searchSpotify(query, type = 'playlist', limit = 10) {
        const accessToken = await getSpotifyAccessToken();

        const response = await fetch(`https://api.spotify.com/v1/search?q=${encodeURIComponent(query)}&type=${type}&limit=${limit}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        const data = await response.json();
        return data.playlists.items || [];
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

        // חישוב העשור שבו האדם היה בן 10
        let decade;
        if (age < 10) {
            decade = 'kids'; // קטגוריה מיוחדת לילדים מתחת לגיל 10
        } else {
            const currentYear = new Date().getFullYear();
            const yearWhenTen = currentYear - age + 10;
            decade = Math.floor(yearWhenTen / 10) * 10;
        }

        // יצירת מחרוזת החיפוש ל-Spotify
        const query = decade === 'kids' ? `kids music` : `${country} ${decade}s hits`;

        console.log(`Search query: ${query}`);
        resultDiv.innerHTML = `<p>Query: ${query}</p>`;

        // חיפוש פלייליסטים ב-Spotify
        const playlists = await searchSpotify(query, 'playlist', 10);

        // בחירת הפלייליסט הראשון
        const closestPlaylist = playlists[0];

        // הצגת התוצאה
        if (closestPlaylist && closestPlaylist.external_urls && closestPlaylist.external_urls.spotify) {
            resultDiv.innerHTML = `
                <p>Your playlist: <a href="${closestPlaylist.external_urls.spotify}" target="_blank">${closestPlaylist.name}</a></p>
                <p>Age detected: ${age}</p>
            `;
        } else {
            resultDiv.innerHTML = '<p>No playlists found, please try again later!</p>';
        }
    });
});

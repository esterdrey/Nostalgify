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

    // חיפוש פלייליסטים ב-Spotify
    let playlists = await searchSpotifyPlaylists(query);

    // אם לא נמצאו פלייליסטים, חיפוש גלובלי
    if (!playlists.length) {
        const globalQuery = decade === 'kids' ? `kids music` : `${decade}s hits`;
        playlists = await searchSpotifyPlaylists(globalQuery);
    }

    // הצגת הפלייליסט הראשון בתוצאה
    if (playlists.length > 0 && playlists[0] && playlists[0].external_urls && playlists[0].external_urls.spotify) {
        const playlist = playlists[0];
        resultDiv.innerHTML = `
            <p>Your playlist: <a href="${playlist.external_urls.spotify}" target="_blank">${playlist.name}</a></p>
            <p>Age detected: ${age}</p>
        `;
    } else {
        resultDiv.innerHTML = '<p>No playlists found, please try again later!</p>';
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const uploadInput = document.getElementById('upload');
    const preview = document.getElementById('preview');
    const submitButton = document.getElementById('submit');
    const resultDiv = document.getElementById('result');
    const countryInput = document.getElementById('country');

    // מפת פלייליסטים לפי מדינה ועשור
    const playlists = {
        "israel_90s": "https://open.spotify.com/playlist/37i9dQZF1DX2FOC3lCipBy",
        "usa_80s": "https://open.spotify.com/playlist/37i9dQZF1DX4UtSsGT1Sbe",
        "uk_70s": "https://open.spotify.com/playlist/37i9dQZF1DWWEJlAGA9gs0"
    };

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

    // חישוב העשור והצגת הפלייליסט
    submitButton.addEventListener('click', () => {
        const country = countryInput.value.trim().toLowerCase();
        const age = 2025 - new Date().getFullYear() + 5;  // גיל משוער
        const decade = Math.floor(age / 10) * 10;

        const key = `${country}_${decade}s`;
        const playlistLink = playlists[key] || "https://open.spotify.com/playlist/37i9dQZF1DX4UtSsGT1Sbe";  // פלייליסט כללי

        resultDiv.innerHTML = `
    <p>Your playlist: <a href="${playlistLink}" target="_blank">Open Playlist</a></p>
    <p>Age detected: ${age}</p>
    `;

    });
});

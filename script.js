document.addEventListener('DOMContentLoaded', async () => {
    const uploadInput = document.getElementById('upload'); // Input element for image upload
    const preview = document.getElementById('preview'); // Image preview element
    const submitButton = document.getElementById('submit'); // Button to submit and process the image
    const resultDiv = document.getElementById('result'); // Div to display the result (playlist)
    const countrySelect = document.getElementById('country'); // Select element for choosing a country

    // List of countries
    const countries = [
        "Argentina", "Australia", "Austria", "Belgium", "Brazil", "Canada", "China", "Colombia", "Denmark",
        "Egypt", "Finland", "France", "Germany", "Greece", "India", "Indonesia", "Ireland", "ישראל", "Italy", 
        "Japan", "Malaysia", "Mexico", "Netherlands", "New Zealand", "Norway", "Philippines", "Poland", "Portugal", 
        "Russia", "Saudi Arabia", "Singapore", "South Africa", "South Korea", "Spain", "Sweden", "Switzerland", 
        "Thailand", "Turkey", "United Kingdom", "United States", "Vietnam"
    ];
    
    // Initialize the country select dropdown with available countries
    function populateCountrySelect() {
        countries.forEach((country) => {
            const option = document.createElement('option');
            option.value = country.toLowerCase(); // Set the value to the lowercase country name
            option.textContent = country; // Display the country name in the dropdown
            countrySelect.appendChild(option);
        });
    }

    // Event listener for country selection change
    countrySelect.addEventListener('change', () => {
        const selectedCountry = countrySelect.value;
        console.log(`Selected country: ${selectedCountry}`); // For debugging purposes
    });
    
    // Image preview functionality: display image when uploaded
    uploadInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                preview.src = e.target.result; // Set the preview image source
                preview.style.display = 'block'; // Display the preview
            };
            reader.readAsDataURL(file); // Read the uploaded file as a data URL
        }
    });

    // Initialize the country select dropdown
    populateCountrySelect();

    // Load the Human.js model from GitHub (used for age detection)
    const human = new Human.Human({
        modelBasePath: 'https://raw.githubusercontent.com/vladmandic/human/main/models', // Path to the model files
        backend: 'webgl', // Use WebGL instead of WebGPU
    });
    await human.load();

    // Function to get an access token from Spotify using client credentials
    async function getSpotifyAccessToken() {
        const clientId = '9e5becb2c8764dada9b60a8f3b3855c6'; // Enter your Spotify Client ID here
        const clientSecret = 'b0de34c77ea64efa9cbf661f08b495e6'; // Enter your Spotify Client Secret here

        const response = await fetch('https://accounts.spotify.com/api/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': 'Basic ' + btoa(clientId + ':' + clientSecret) // Basic Auth for client credentials
            },
            body: 'grant_type=client_credentials' // Grant type for access token request
        });

        const data = await response.json();
        return data.access_token; // Return the access token
    }

    // Function to search for Spotify playlists based on a query string
    async function searchSpotifyPlaylists(query) {
        const accessToken = await getSpotifyAccessToken(); // Get the Spotify Access Token

        const response = await fetch(`https://api.spotify.com/v1/search?q=${encodeURIComponent(query)}&type=playlist`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}` // Use the access token to authenticate the request
            }
        });

        const data = await response.json();
        return data.playlists.items; // Return the list of playlists found
    }

    // Event listener for the submit button to process the uploaded image
    submitButton.addEventListener('click', async () => {
        const country = countrySelect.value.trim().toLowerCase(); // Get the selected country value

        if (!preview.src) { // Check if an image has been uploaded
            alert('Please upload an image.');
            return;
        }

        // Create a new Image object to load the uploaded image
        const img = new Image();
        img.src = preview.src;
        await img.decode(); // Wait for the image to load and decode

        // Use Human.js to detect the face and estimate age
        const result = await human.detect(img);

        if (result.face.length === 0) { // If no face is detected
            alert('No face detected. Please upload a clear image.');
            return;
        }

        const age = Math.round(result.face[0].age); // Round the age detected

        // Calculate the decade when the person was 10 years old
        let decade;
        if (age < 10) {
            decade = 'kids'; // Special category for people under 10 years old
        } else {
            const currentYear = new Date().getFullYear(); // Get the current year
            const yearWhenTen = currentYear - age + 10; // Calculate the year the person was 10
            decade = Math.floor(yearWhenTen / 10) * 10; // Get the decade when the person was 10
        }

        // Create a search query string for Spotify based on the decade and country
        const query = decade === 'kids' ? `${country} kids music` : `${country} ${decade}`;

        // Search for playlists on Spotify based on the query
        const playlists = await searchSpotifyPlaylists(query);

        // Display the first playlist in the search results
        if (playlists.length > 0 && playlists[0]?.external_urls?.spotify) {
            const playlist = playlists[0]; // Get the first playlist
            resultDiv.innerHTML = `
                <p>Your playlist: <a href="${playlist.external_urls.spotify}" target="_blank">${playlist.name}</a></p>
            `;
        } else {
            const dummy_query = decade === 'kids' ? `kids music` : `${decade}`; // Fallback search query
            const dummy_playlists = await searchSpotifyPlaylists(dummy_query);
            const dummy_playlist = dummy_playlists[0]; // Get the first fallback playlist
            resultDiv.innerHTML = `
                <p>No playlists found for your country, so enjoy global nostalgic hits: <a href="${dummy_playlist.external_urls.spotify}" target="_blank">${dummy_playlist.name}</a></p>
            `;
        }
    });
});

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1,maximum-scale=1,user-scalable=no">
    <title>GoogleProto - Map with Weather, ETA & Traffic</title>

    <!-- Favicon -->
    <link rel="icon" href="C:\Users\sandh\GoogleProto\GoogleProto\istockphoto-873392482-612x612.jpg" type="x-icon">

    <!-- Highlighted Link to TomTom Traffic Index -->
    <div style="position: absolute; top: 90px; right: 50px; z-index: 1000;">
    <a href="https://www.tomtom.com/traffic-index/chennai-traffic/" target="_blank" style="background-color: red; padding: 10px; border-radius: 5px; text-decoration: none; color: white; font-weight: bold;">Check Chennai Traffic Index</a>
    </div>

    <!-- Mapbox CSS -->
    <link href="https://api.mapbox.com/mapbox-gl-js/v2.10.0/mapbox-gl.css" rel="stylesheet">
    <script src="https://api.mapbox.com/mapbox-gl-js/v2.10.0/mapbox-gl.js"></script>

    <!-- Mapbox Directions Plugin -->
    <script src="https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-directions/v4.0.0/mapbox-gl-directions.js"></script>
    <link rel="stylesheet" href="https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-directions/v4.0.0/mapbox-gl-directions.css">

    <style>
        body { margin: 0; padding: 0; font-family: Arial, sans-serif; }
        #map { position: absolute; top: 0; bottom: 0; width: 100%; }

        /* Info Boxes */
        .info-box { 
            position: absolute;
            background: white;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 0 5px rgba(0,0,0,0.3);
            font-size: 14px;
            z-index: 999;
            width: 220px;
        }

        /* Positioning Each Info Box */
        #weather-start { top: 20px; left: 320px; }  /* Adjusted position */
        #weather-destination { top: 20px; right: 50px; }
        #eta-box { bottom: 20px; left: 20px; }
        #traffic-box { bottom: 20px; right: 20px; }
    </style>
</head>
<body>

    <!-- Map Container -->
    <div id="map"></div>

    <!-- Separate Dialog Boxes for Each Detail -->
    <div id="weather-start" class="info-box">Fetching starting location weather...</div>
    <div id="weather-destination" class="info-box">Fetching destination weather...</div>
    <div id="eta-box" class="info-box">Calculating ETA...</div>
    <div id="traffic-box" class="info-box">Loading live traffic...</div>

    <script>
        // API Keys
        mapboxgl.accessToken = 'your_mapbox_access_token'; // Replace with your Mapbox Token
        const openWeatherKey = 'your_openweather_keytoken'; // Replace with your OpenWeatherMap API Key

        // Initialize the Map with Traffic Layer
        const map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/navigation-day-v1',
            center: [77.2090, 28.6139], // Default center (New Delhi, India)
            zoom: 10
        });

        // Add Controls
        const directions = new MapboxDirections({
            accessToken: mapboxgl.accessToken,
            unit: 'metric',
            profile: 'mapbox/driving'
        });
        map.addControl(directions, 'top-left');
        map.addControl(new mapboxgl.FullscreenControl(), 'top-right');
        map.addControl(new mapboxgl.NavigationControl(), 'top-right');

        // Function to Fetch Weather Data
        function fetchWeather(lat, lon, elementId, locationName) {
            const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${openWeatherKey}&units=metric`;

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    if (data.weather && data.main) {
                        document.getElementById(elementId).innerHTML =
                            `<b>${locationName} Weather</b><br>
                             ${data.weather[0].description}, ${data.main.temp}°C`;
                    } else {
                        document.getElementById(elementId).innerHTML = "Weather data unavailable";
                    }
                })
                .catch(error => {
                    console.error(`Error fetching weather for ${locationName}:`, error);
                    document.getElementById(elementId).innerHTML = "Error loading weather";
                });
        }

        // Get User's Current Location
navigator.geolocation.getCurrentPosition(
    (position) => {
        const userCoords = [position.coords.longitude, position.coords.latitude];
        map.setCenter(userCoords);

        // Add a marker for user's location
        new mapboxgl.Marker({ color: 'red' })
            .setLngLat(userCoords)
            .setPopup(new mapboxgl.Popup().setHTML("<b>You are here</b>"))
            .addTo(map);

        // Fetch weather for current location
        fetchWeather(userCoords[1], userCoords[0], "weather-start", "Current Location");
    },
    (error) => {
        console.error("Error getting user location:", error);
        document.getElementById('weather-start').innerHTML = "Could not fetch current location.";
    },
    { enableHighAccuracy: true }
);
        // Fetch ETA Based on Live Traffic
        function fetchETA(start, end) {
            const url = `https://api.mapbox.com/directions/v5/mapbox/driving/${start[0]},${start[1]};${end[0]},${end[1]}?access_token=${mapboxgl.accessToken}&geometries=geojson`;

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    if (data.routes && data.routes.length > 0) {
                        const duration = data.routes[0].duration / 60; // Convert seconds to minutes
                        document.getElementById('eta-box').innerHTML = `<b>ETA:</b> ${Math.round(duration)} minutes`;
                    } else {
                        document.getElementById('eta-box').innerHTML = "ETA unavailable";
                    }
                })
                .catch(error => {
                    console.error("Error fetching ETA:", error);
                    document.getElementById('eta-box').innerHTML = "Error loading ETA";
                });
        }

        // Fetch Live Traffic Conditions
        function fetchTrafficConditions(start, end) {
            const trafficUrl = `https://api.mapbox.com/directions/v5/mapbox/driving/${start[0]},${start[1]};${end[0]},${end[1]}?access_token=${mapboxgl.accessToken}&overview=full&annotations=congestion`;

            fetch(trafficUrl)
                .then(response => response.json())
                .then(data => {
                    if (data.routes && data.routes.length > 0) {
                        const congestion = data.routes[0].legs[0].annotation.congestion;
                        document.getElementById('traffic-box').innerHTML =
                            `<b>Traffic Update:</b> ${congestion[0] || "Moderate Traffic"}`;
                    } else {
                        document.getElementById('traffic-box').innerHTML = "Traffic data unavailable";
                    }
                })
                .catch(error => {
                    console.error("Error fetching traffic:", error);
                    document.getElementById('traffic-box').innerHTML = "Error loading traffic";
                });
        }

        // Listen for Route Changes and Fetch Weather, ETA & Traffic
        directions.on('route', (event) => {
            if (event.route.length > 0) {
                const start = directions.getOrigin().geometry.coordinates;
                const end = directions.getDestination().geometry.coordinates;

                // Fetch Weather for Start & End Locations
                fetchWeather(start[1], start[0], "weather-start", "Starting Location");
                fetchWeather(end[1], end[0], "weather-destination", "Destination");

                // Fetch ETA
                fetchETA(start, end);

                // Fetch Traffic Conditions
                fetchTrafficConditions(start, end);
            }
        });

        // Get User's Current Location
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const userCoords = [position.coords.longitude, position.coords.latitude];
                map.setCenter(userCoords);

                // Add a marker for user's location
                new mapboxgl.Marker({ color: 'red' })
                    .setLngLat(userCoords)
                    .setPopup(new mapboxgl.Popup().setHTML("<b>You are here</b>"))
                    .addTo(map);

                // Fetch weather for current location
                fetchWeather(userCoords[1], userCoords[0], "weather-start", "Current Location");
            },
            (error) => {
                console.error("Error getting user location:", error);
                document.getElementById('weather-start').innerHTML = "Could not fetch current location.";
            },
            { enableHighAccuracy: true }
        );

        // Fetch Live Traffic Updates Every 1 Minute
        setInterval(() => {
            const start = directions.getOrigin().geometry.coordinates;
            const end = directions.getDestination().geometry.coordinates;
            if (start && end) {
                fetchTrafficConditions(start, end);
            }
        }, 60000);
    </script>

</body>
</html>

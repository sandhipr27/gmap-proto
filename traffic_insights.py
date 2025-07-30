<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Traffic Insights</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://api.mapbox.com/mapbox-gl-js/v2.14.1/mapbox-gl.js"></script>
    <link href="https://api.mapbox.com/mapbox-gl-js/v2.14.1/mapbox-gl.css" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #2f3b52;
            color: #fff;
        }
        header {
            background-color: #4e73df;
            padding: 20px;
            text-align: center;
        }
        h1.animated-title {
            font-size: 36px;
            color: #fff;
            animation: pulse 2s infinite;
        }
        nav ul {
            list-style: none;
            padding: 0;
            margin-top: 10px;
        }
        nav ul li {
            display: inline;
            margin: 0 15px;
        }
        nav ul li a {
            color: #fff;
            text-decoration: none;
            font-size: 18px;
        }
        nav ul li a:hover {
            color: #ffcc00;
        }

        .card {
            margin: 20px;
            padding: 20px;
            background-color: #35424a;
            border-radius: 10px;
        }

        .map-container {
            height: 400px;
            width: 100%;
        }

        .chart-container {
            width: 100%;
            height: 400px;
            margin-top: 30px;
        }

        .progress-bar-container {
            margin: 30px 0;
            padding: 20px;
            background-color: #4e73df;
            border-radius: 5px;
        }
        .progress-bar {
            height: 20px;
            background-color: #ff5733;
            width: 0;
            transition: width 1s ease-in-out;
        }

        footer {
            text-align: center;
            padding: 10px;
            background-color: #4e73df;
        }

        /* Animations */
        @keyframes pulse {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.1);
            }
            100% {
                transform: scale(1);
            }
        }

        /* Badge Styles */
        .badge {
            background-color: #ffcc00;
            border-radius: 50%;
            padding: 10px;
            font-size: 20px;
            color: #333;
            position: absolute;
            top: 20px;
            right: 20px;
        }

    </style>
</head>
<body>

    <header>
        <h1 class="animated-title" id="logo">🚦 Traffic Insights 🎮</h1>
        <nav>
            <ul>
                <li><a href="#past">📜 Past Data</a></li>
                <li><a href="#present">🌍 Live Traffic</a></li>
                <li><a href="#future">🔮 Predictions</a></li>
            </ul>
        </nav>
    </header>
    
    <section id="present" class="card">
        <h2>Live Traffic</h2>
        <div id="map" class="map-container"></div>
        <div class="badge" id="badge">+50 XP</div>
    </section>
    
    <section id="past" class="card">
        <h2>Past Traffic Data</h2>
        <div class="chart-container">
            <canvas id="intensityChart"></canvas>
        </div>
        <div class="chart-container">
            <canvas id="travelTimeChart"></canvas>
        </div>
    </section>
    
    <section id="future" class="card">
        <h2>Traffic Predictions</h2>
        <div class="chart-container">
            <canvas id="historicDataChart"></canvas>
        </div>
    </section>

    <section class="progress-bar-container">
        <h3>Experience Level</h3>
        <div class="progress-bar" id="progressBar"></div>
    </section>
    
    <footer>
        <p>&copy; 2025 Traffic Insights | Level Up Your Commute 🎖️</p>
    </footer>
    
    <script>
        mapboxgl.accessToken = 'YOUR_MAPBOX_ACCESS_TOKEN';
        var map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/dark-v10',
            center: [0, 0],
            zoom: 2
        });

        // Traffic Intensity Chart
        var ctx1 = document.getElementById('intensityChart').getContext('2d');
        var intensityChart = new Chart(ctx1, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Traffic Intensity',
                    data: [30, 50, 70, 90, 60, 80],
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    fill: true
                }]
            }
        });

        // Average Travel Time Chart
        var ctx2 = document.getElementById('travelTimeChart').getContext('2d');
        var travelTimeChart = new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: ['Morning', 'Afternoon', 'Evening', 'Night'],
                datasets: [{
                    label: 'Average Travel Time (mins)',
                    data: [45, 30, 60, 20],
                    backgroundColor: ['#FF5733', '#FFC300', '#28A745', '#007BFF']
                }]
            }
        });

        // Historic Data Chart
        var ctx3 = document.getElementById('historicDataChart').getContext('2d');
        var historicDataChart = new Chart(ctx3, {
            type: 'line',
            data: {
                labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
                datasets: [{
                    label: 'Historic Traffic Data',
                    data: [100, 120, 90, 110, 130, 140],
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    fill: true
                }]
            }
        });

        // Update Progress Bar and Badge
        function updateProgressBar() {
            const progressBar = document.getElementById('progressBar');
            let currentWidth = progressBar.style.width;
            currentWidth = currentWidth ? parseInt(currentWidth) : 0;
            if (currentWidth < 100) {
                progressBar.style.width = (currentWidth + 10) + '%';
            }
        }

        setInterval(updateProgressBar, 3000); // Simulate progress over time
    </script>
</body>
</html>

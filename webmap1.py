<html>
    <head>
        <title>GoogleProto</title>
        <meta name="viewport" content="intial-scale=1,maximum-scale=1,user-scalable=no">
        <link href="https://api.mapbox.com/mapbox-gl-js/v2.10.0/mapbox-gl.css" rel="stylesheet">
        <script src='https://api.mapbox.com/mapbox-gl-js/v2.10.0/mapbox-gl.js'></script>
        <style>
            body { margin: 0; padding: 0; }
            #map { position: absolute; top: 0; bottom: 0; width: 100% }
        </style>
    </head>
    <body>
        <script src="https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-directions/v4.1.0/mapbox-gl-directions.js"></script>
        <link rel="stylesheet" href="https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-directions/v4.1.0/mapbox-gl-directions.css" type="text/css">
        <div id="map"></div>
        <script>
            mapboxgl.accessToken ='your-mapbox-accesstoken'
            const map = new mapboxgl.Map({
                container: 'map',
                style: 'mapbox://styles/mapbox/streets-v11',
                center: [-110, 45],
                zoom: 4
            });
            const marker1 = new mapboxgl.Marker()
                .setLngLat([-110,45])
                .addTo(map);
            const marker2 = new mapboxgl.Marker({
                color: 'red',
                rotation: 0
            })
            .setLngLat([-112, 42])
            .addTo(map);
            map.addControl(new mapboxgl.FullscreenControl(), 'top-right');
            map.addControl(new mapboxgl.NavigationControl(), 'top-right');
            map.addControl(
                new MapboxDirections({
                    accessToken: mapboxgl.accessToken
                    }), 'top-left'
            );
        </script>
    </body>
</html>


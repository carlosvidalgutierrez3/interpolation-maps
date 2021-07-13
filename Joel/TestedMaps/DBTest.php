<!---------------------------------------PLEASE, DO NOT CHANGE HTML IN THIS FILE!--------------------------------
-----------------------------------------PLEASE, DO NOT CHANGE HTML IN THIS FILE!--------------------------------
-----------------------------------------PLEASE, DO NOT CHANGE HTML IN THIS FILE!--------------------------------
-----------------------------------------PLEASE, DO NOT CHANGE HTML IN THIS FILE!-------------------------------- -->

<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8" />
    <title>PAE Map</title>
    <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no" />
    <script src="https://api.mapbox.com/mapbox-gl-js/v1.9.0/mapbox-gl.js"></script>
    <link href="https://api.mapbox.com/mapbox-gl-js/v1.9.0/mapbox-gl.css" rel="stylesheet" />
    <style>
        /* -----------------------------------------PLEASE, DO NOT CHANGE CSS CODE IN THIS FILE!-------------------------------- */
        /* -----------------------------------------PLEASE, DO NOT CHANGE CSS CODE IN THIS FILE!-------------------------------- */
        /* -----------------------------------------PLEASE, DO NOT CHANGE CSS CODE IN THIS FILE!-------------------------------- */
        /* -----------------------------------------PLEASE, DO NOT CHANGE CSS CODE IN THIS FILE!-------------------------------- */
        body {
            margin: 0;
            padding: 0;
        }

        #map {
            position: absolute;
            top: 50px;
            bottom: 0;
            width: 90%;
        }

        #menu {
            background: #fff;
            position: absolute;
            z-index: 1;
            top: 10px;
            right: 10px;
            border-radius: 3px;
            width: 120px;
            border: 1px solid rgba(0, 0, 0, 0.4);
            font-family: 'Open Sans', sans-serif;
        }

        #menu a {
            font-size: 13px;
            color: #404040;
            display: block;
            margin: 0;
            padding: 0;
            padding: 10px;
            text-decoration: none;
            border-bottom: 1px solid rgba(0, 0, 0, 0.25);
            text-align: center;
        }

        #menu a:last-child {
            border: none;
        }

        #menu a:hover {
            background-color: #f8f8f8;
            color: #404040;
        }

        #menu a.active {
            background-color: #3887be;
            color: #ffffff;
        }

        #menu a.active:hover {
            background: #3074a4;
        }
    </style>
</head>

<body>

    <?php
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "bsinfo";
    $port = "3308";

    $conn = new mysqli($servername, $username, $password, $dbname, $port);

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $sql = "SELECT latitud, longitud, pes FROM valors";
    $result = mysqli_query($conn, $sql);

    $data = array();
    while ($enr = mysqli_fetch_assoc($result)) {
        $a = array($enr['latitud'], $enr['longitud'], $enr['pes']);
        array_push($data, $a);
    }


    ?>

    <nav id="menu"></nav>
    <div id="map"></div>

    <script>
        //-------------------------------------PLEASE, DEVELOP MAP ONLY IN THIS FILE--------------------------------------------
        //-------------------------------------PLEASE, DEVELOP MAP ONLY IN THIS FILE--------------------------------------------
        //-------------------------------------PLEASE, DEVELOP MAP ONLY IN THIS FILE--------------------------------------------
        //-------------------------------------PLEASE, DEVELOP MAP ONLY IN THIS FILE--------------------------------------------



        //----------------------------------------------JS CODE STARTS HERE------------------------------------------------------

        var dades = <?php echo json_encode($data); ?>;

        //Necessary token for maps creation (Always use the same!)
        mapboxgl.accessToken = 'pk.eyJ1IjoieXVndWkiLCJhIjoiY2s4ZGdpOGxuMGFuYjNmcGd2bGhnZGZkMCJ9.9B0gzmUBMNyI6RJDfEBPGQ';

        //Create map centered on BCN, with the style and zoom chosen
        var map = new mapboxgl.Map({
            container: 'map',
            style: 'mapbox://styles/mapbox/light-v10', //"light" can be replaced by "dark" (background style)
            center: [2.154, 41.39],
            zoom: 5,
        });


        //Add a listener to the mouse cursor movement. It saves the coordinates where it is located.
        var coordinates;

        map.on('mousemove', function(e) {

            coordinates = e.lngLat.wrap();
        });

        //Idea: show data value when user clicks anywhere. Marker needed?
        var marker = new mapboxgl.Marker();

        function animateMarker() {

            //Set marker at mouse cursor coordinates
            marker.setLngLat(coordinates);

            //Ensure the marker is added to the map.
            marker.addTo(map);

            //Request the next frame of the animation.
            requestAnimationFrame(animateMarker);
        }

        map.on('load', function() {
            var layers = map.getStyle().layers;

            var labelLayerId;
            for (var i = 0; i < layers.length; i++) {
                if (layers[i].type === 'symbol' && layers[i].layout['text-field']) {
                    labelLayerId = layers[i].id;
                    break;
                }
            }

            //Create a GeoJSON with points inside. Modify this variable for testing other coordinates.
            //Notice the JSON cannot be imported locally due to CORS policy problems. Once database
            //is working, this problem will be solved. Therefore, by the moment the way to visualise
            //data is by including it directly in this variable.

            var geojson =  {
                "type": "FeatureCollection",
                "features": []
            };


            for (var i = 0; i < dades.length; i++) {
                geojson.features.push({
                    "geometry": {
                        "type": "Point",
                        "coordinates": [dades[i][0], dades[i][1]]
                    },
                    "type": "Feature",

                    "properties": {
                        "FIELD3": parseFloat(dades[i][2])
                    }
                })

            };





            //Add the GeoJSON point source.
            //This data will only be used to create the CirclesMap

            map.addSource('intdata', {
                'type': 'geojson',
                'data': geojson
            });



            //Creates an empty JSON for future SquaresMap data

            var geojsonmap = {
                "type": "FeatureCollection",
                "features": []
            };


            //Using Points from geojson variable, creates 5 coordinates and adds them to the empty geojsonmap JSON
            //As L2 has a resolution of 0.1 degrees, Points need to be placed in four different positions since
            //the ones on geojson in distances of 0.05 degrees both in latitude and longitude

            for (var i = 0; i < geojson.features.length; i++) {
                geojsonmap.features.push({
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [parseFloat(geojson.features[i].geometry.coordinates[0]) - 0.05, parseFloat(geojson.features[i].geometry.coordinates[1]) - 0.05],
                                [parseFloat(geojson.features[i].geometry.coordinates[0]) + 0.05, parseFloat(geojson.features[i].geometry.coordinates[1]) - 0.05],
                                [parseFloat(geojson.features[i].geometry.coordinates[0]) + 0.05, parseFloat(geojson.features[i].geometry.coordinates[1]) + 0.05],
                                [parseFloat(geojson.features[i].geometry.coordinates[0]) - 0.05, parseFloat(geojson.features[i].geometry.coordinates[1]) + 0.05],
                                [parseFloat(geojson.features[i].geometry.coordinates[0]) - 0.05, parseFloat(geojson.features[i].geometry.coordinates[1]) - 0.05]
                            ]
                        ]
                    },


                    "properties": {
                        "FIELD3": parseFloat(geojson.features[i].properties.FIELD3)
                    }
                })

            };


            //Use the GeoJSON created to add a Polygon source (contains SquareMap data)

            map.addSource('intdatasquares', {
                'type': 'geojson',
                'data': geojsonmap
            });


            //Add the SquaresMap layer

            map.addLayer({
                'id': 'SquaresMap',
                'type': 'fill',
                'source': 'intdatasquares',
                'paint': {
                    'fill-color': { //Generates the color gradient to represent. Same than CirclesMap.
                        property: 'FIELD3',
                        type: 'exponential',
                        stops: [
                            [0, '#21DC32'],
                            [1.5, '#F1F908'],
                            [3, '#F98B08'],
                            [5, '#F90808'],
                            [7.5, '#9308F9'],
                            [10, '#6C080B']
                        ]
                    },
                    'fill-opacity': 0.5, //Adjust the opacity of squares
                    'fill-antialias': false //Make the borders to not overlap (darker color appears if not)
                    //'fill-outline-color': '#000000' //Create a border color
                }
            });



            //Add the 3D Buildings layer. Maybe a smoother 2D-3D transition could be added.
            //To be determined

            map.addLayer({
                    'id': '3d-buildings',
                    'source': 'composite',
                    'source-layer': 'building',
                    'filter': ['==', 'extrude', 'true'],
                    'type': 'fill-extrusion',
                    'paint': {
                        'fill-extrusion-color': '#aaa',

                        // use an 'interpolate' expression to add a smooth transition effect to the
                        // buildings as the user zooms in
                        'fill-extrusion-height': [
                            'interpolate',
                            ['linear'],
                            ['zoom'],
                            15,
                            0,
                            15.05,
                            ['get', 'height']
                        ],
                        'fill-extrusion-base': [
                            'interpolate',
                            ['linear'],
                            ['zoom'],
                            15,
                            0,
                            15.05,
                            ['get', 'min_height']
                        ],
                        'fill-extrusion-opacity': 0.6
                    }
                },
                labelLayerId
            );



            //Add the CirclesMap layer.

            map.addLayer({
                'id': 'CirclesMap',
                'type': 'circle',
                'source': 'intdata',
                'paint': {
                    'circle-radius': {
                        'base': 1,
                        'stops': [
                            //Specify the radius for each zoom in the form [zoom, radius]. Works with stops, for example: from
                            //zoom 1 to 2.51 the circle radius will be 0.8. Needs to be optimized.
                            [1, 0.8],
                            [2.5137837820787894, 1.3],
                            [3.0316415551140667, 2],
                            [3.480928067025637, 2.5],
                            [3.8062606913022594, 3.3],
                            [4.255547203213881, 4],
                            [5, 8],
                            [5.302824376136311, 11],
                            [5.60069869997978, 13],
                            [5.774619136188248, 15.5],
                            [6.289270246202039, 18],
                            [6.834504452665333, 25],
                            [7.253624625174822, 35],
                            [7.725419385226766, 50],
                            [8, 75],
                            [8.482480325567531, 100],
                            [9.315365803914922, 200],
                            [10.415722378758561, 400],
                            [15.091313659080143, 10000]
                        ]
                    },


                    'circle-color': { //Generates the color gradient to represent. Same than SquaresMap.
                        property: 'FIELD3',
                        type: 'exponential',
                        stops: [
                            [0, '#21DC32'],
                            [1.5, '#F1F908'],
                            [3, '#F98B08'],
                            [4.5, '#F90808'],
                            [6, '#9308F9'],
                            [7.5, '#6C080B']
                        ]
                    },

                    'circle-opacity': 0.4, //Adjust the opacity of circles
                    'circle-blur': 1, //Adjust the blurring of circles
                    'circle-pitch-alignment': 'map', //When 3D is allowed, circles will be aligned with floor level
                }
            });
        });

        //Allows the user layer control and relates its menu with the correspondent CSS code

        var toggleableLayerIds = ['SquaresMap', 'CirclesMap'];

        for (var i = 0; i < toggleableLayerIds.length; i++) {
            var id = toggleableLayerIds[i];

            var link = document.createElement('a');
            link.href = '#';
            link.className = 'active';
            link.textContent = id;

            link.onclick = function(e) {
                var clickedLayer = this.textContent;
                e.preventDefault();
                e.stopPropagation();

                var visibility = map.getLayoutProperty(clickedLayer, 'visibility');

                if (visibility === 'visible') {
                    map.setLayoutProperty(clickedLayer, 'visibility', 'none');
                    this.className = '';
                } else {
                    this.className = 'active';
                    map.setLayoutProperty(clickedLayer, 'visibility', 'visible');
                }
            };

            var layers = document.getElementById('menu');
            layers.appendChild(link);
        }

        //Starts the first frame of Marker

        requestAnimationFrame(animateMarker);

        //------------------------------------------------JS CODE ENDS HERE----------------------------------------------
    </script>

    <button onclick="knowZoom()">Show current zoom</button>

    <script>
        function knowZoom() {
            alert("The current zoom is " + map.getZoom());
        }
    </script>


    <button onclick="boundsCoordinates()">Show bounds coordinates</button>

    <script>
        function boundsCoordinates() {
            alert("The bounds coordinates are " + map.getBounds());
        }
    </script>



</body>

</html>
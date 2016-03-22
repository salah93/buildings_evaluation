var panorama;
var building;
$('.submit').on('click', function(){
    $.getJSON("/_get_points", {
        address: $('.address').val(),
        nearby: $('select.search_query').val()
    }, function(data) {
        console.log("finished")
        $('.result').html("<div id=map></div><div class='floating-panel'><input type='button' value='Toggle Street View' onclick='toggleStreetView();'></input></div>");
        building = {lat: data.address.latitude, lng: data.address.longitude};
        var map = new google.maps.Map(document.getElementById('map'), {
            center: building,
            minZoom: 16,
            maxZoom: 18,
            zoom: 17,
            scrollwheel: false,
            streetViewControl: false
        });

        for(var i = 0; i < data.points.length; i++){
            create_marker(data.points[i]);
        }

        function create_marker(place_data){
            var circle = new google.maps.Marker({
                position: {lat: place_data['latitude'],
                           lng: place_data['longitude']},
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    strokeOpacity: 1.0,
                    strokeColor: 'black',
                    strokeWeight: 3.0,
                    fillColor: place_data['color'],
                    fillOpacity: 0.6,
                    scale: place_data['radius']
                },
                map: map
            });

            var infowindow = new google.maps.InfoWindow({
                content: place_data['description']
            });

            google.maps.event.addListener(circle, 'click', function() {
                infowindow.open(map, circle);
            });

            google.maps.event.addListener(map, 'click', function() {
                infowindow.close();
            });
        }

        panorama = map.getStreetView();
    })
});

function toggleStreetView(){
    var toggle = panorama.getVisible();
    if (toggle == false) {
        panorama.setPosition(building);
        panorama.setPov(({
            heading: 265,
            pitch: 0
        }));
        panorama.setVisible(true);
    } else {
        panorama.setVisible(false);
    }
}

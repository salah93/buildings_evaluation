$('.submit').on('click', function(){
    $.getJSON("/_get_points", {
        address: $('.address').val(),
        search_query: $('#search_query').val()
    }, function(data) {
        $('.result').html("<div id=map></div>");

        var map = L.map('map', {
            center: [data.address.latitude,
                     data.address.longitude],
            minZoom: 16,
            maxZoom: 18,
            zoom: 17
        });

        L.tileLayer('https://{s}.tiles.mapbox.com/v4/salah93.lekj6ig9/{z}/{x}/{y}.png?access_token=pk.eyJ1Ijoic2FsYWg5MyIsImEiOiJBV25DdnhFIn0.qpwe2xvEpTy_mO4wxzp5nQ' , {
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>, Salah\'s map'
        }).addTo(map);

        for(var i = 0; i < data.points.length; i++){
            var circle = L.circle([data.points[i]['latitude'], 
                                   data.points[i]['longitude']], 
                                   data.points[i]['radius'], {
                    color: data.points[i]['color'],
                    fillColor: data.points[i]['color'],
            }).bindPopup(data.points[i]['description']).addTo(map);
        }

        /*
        map.scrollWheelZoom.disable();
        */
    })
});




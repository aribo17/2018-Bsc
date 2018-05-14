$(document).ready(function() {

    var mymap = L.map('map').setView([58.969, 5.73], 10);

    var osm = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png',
    {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'}).addTo(mymap);

    mymap.addLayer(osm);

    var oReq = new XMLHttpRequest();
    var data;
    var c_data = []; // list of all events
    oReq.open("GET", '/auth/get_event_location_data', true);
    oReq.send();

    oReq.onreadystatechange = function() {
        if (oReq.readyState == 4 && oReq.status == 200) {
            data = JSON.parse(oReq.responseText);
            console.log(data)


            var temp_obj = {}
            for(var i=0; i<Object.keys(data).length;i++){
              temp_obj= {
                title:data[i][0].name,
                latitude:data[i][1].latitude,
                longitude:data[i][1].longitude,
                photo:data[i][0].photo
              };
              c_data.push(temp_obj);
            };

            var markers = [];

            for (var key in c_data) {
                // check if the property/key is defined in the object itself, not in parent
                if (c_data.hasOwnProperty(key)) {
                    //console.log(key, c_data[key]);

                    var marker = new L.Marker([c_data[key].latitude, c_data[key].longitude]);
                    mymap.addLayer(marker)
                    marker.bindPopup(c_data[key].title + "<br><img height='45' width='45' src='static/images/"+c_data[key].photo+"'/>");

                }
            }
            console.log(markers)
        }
    }




});

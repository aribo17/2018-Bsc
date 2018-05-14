function eventData(){
  var xhr = new XMLHttpRequest();
  xhr.open("GET", '/auth/get_event_location_data', true);

  xhr.onreadystatechange = function(){
    if(xhr.readyState == 4 && xhr.status == 200){
      var result = JSON.parse(xhr.responseText);
      console.log(result)
      var data = []
      var temp_obj = {}
      for(var i=0; i<Object.keys(result).length;i++){
        temp_obj= {
          title:result[i].name,
          lat:result[i].latitude,
          lng:result[i].longitude
        };
        data.push(temp_obj);
        console.log(data)
    }
  };
  //xhttp.open("GET","/map",true);
  //xhttp.send();
}
}


$(document).ready(function initMap(){
    //var data = JSON.parse(document.getElementById('jsondata_map').dataset.location); /*AJAX. Data rett fra python */
    //console.log(data)
    eventData()
      // Map options

      var options = {
        zoom:11,
        center:{lat: 58.97005, lng:5.73332}
      };

      // New map
      var map = new google.maps.Map(document.getElementById('map'), options);

      // Listen for click on map
      google.maps.event.addListener(map, 'click', function(event){
        // Add marker
        addMarker({coords:event.latLng});
      });

      var center = {
        lat:58.963333,
        lng:5.718889
      };
      // Define the rectangle and set its editable property to true.
      var circle = new google.maps.Circle({
        center: center,
        radius:1000,
        editable: true,
        draggable: true
      });

      circle.setMap(map);

      // Add an event listener on the rectangle.
      circle.addListener('center_changed', showNewCircle);
      circle.addListener('radius_changed', showNewCircle);

      // Define an info window on the map.
      infoWindow = new google.maps.InfoWindow();

    // Show the new coordinates for the rectangle in an info window.

    // @this {google.maps.Rectangle} //
    var data = {};
    function showNewCircle(event) {
      var newCenter = circle.getCenter();
      var newRadius = circle.getRadius();

      // data = {newCenter, newRadius};

      // var contentString = '<b>Circle moved.</b><br>' +
      //     'New center: ' + newCenter.lat + '<br>' +
      //     'New south-west corner: ' + newRad.lat() + ', ' + sw.lng();

      // Set the info window's content and position.
      // infoWindow.setContent(contentString);
      infoWindow.setCenter(newCenter);
      infoWindow.setRadius(newRadius);

      infoWindow.open(map);
    }

      /*
      // Add marker
      var marker = new google.maps.Marker({
        position:{lat:42.4668,lng:-70.9495},
        map:map,
        icon:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png'
      });

      var infoWindow = new google.maps.InfoWindow({
        content:'<h1>Lynn MA</h1>'
      });

      marker.addListener('click', function(){
        infoWindow.open(map, marker);
      });
      */

      // Array of markers
      var markers = [
        {
          coords:{lat:42.4668,lng:-70.9495},
          iconImage:'https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png',
          content:'<h1>Lynn MA</h1>'
        },
        {
          coords:{lat:42.8584,lng:-70.9300},
          content:'<h1>Amesbury MA</h1>'
        },
        {
          coords:{lat:42.7762,lng:-71.0773}
        }
      ];

      // Loop through markers
      for(var i = 0;i < markers.length;i++){
        // Add marker
        addMarker(markers[i]);
      }

      // Add Marker Function
      function addMarker(props){
        var marker = new google.maps.Marker({
          position:props.coords,
          map:map,
          //icon:props.iconImage
        });

        // Check for customicon
        if(props.iconImage){
          // Set icon image
          marker.setIcon(props.iconImage);
        }

        // Check content
        if(props.content){
          var infoWindow = new google.maps.InfoWindow({
            content:props.content
          });

          marker.addListener('click', function(){
            infoWindow.open(map, marker);
          });
        }
    }
});


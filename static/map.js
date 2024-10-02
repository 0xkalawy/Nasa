let lng, lat, map, marker;
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        const userLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };

        // Create the map centered at the user's location
        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 14,
            center: userLocation
        });

        // Add a marker at the user's location
        marker = new google.maps.Marker({
            position: userLocation,
            map: map,
            title: 'You are here!'
        });
    }, function(error) {
        handleLocationError(true);
    });
} else {
    handleLocationError(false);
}

function searchLocation(query) {
    const service = new google.maps.places.PlacesService(map);
    service.textSearch({ query: query }, function(results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            const place = results[0]; // Get the first result
            const location = place.geometry.location;

            // Update map center and place marker
            map.setCenter(location);
            placeMarker(location, place.name);
        } else {
            alert('Place not found: ' + status);
        }
    });
}

function searchByLatLng(lat, lng) {
    const location = new google.maps.LatLng(lat, lng);
    map.setCenter(location);
    placeMarker(location, `Latitude: ${lat}, Longitude: ${lng}`);
}

function placeMarker(location, title = `Selected Location: ${location.lat()}, ${location.lng()}`) {
    // If a marker already exists, remove it
    if (marker) {
        marker.setMap(null);
    }

    // Create a new marker at the clicked location
    marker = new google.maps.Marker({
        position: location,
        map: map,
        title: title
    });

    // Display the selected latitude and longitude
    document.getElementById('placeLngLat').innerText = 'Selected Location:\n' + location.lat() + "\n" + location.lng();
    lng = location.lng();
    lat = location.lat();            
}

function handleLocationError(browserHasGeolocation) {
    alert(browserHasGeolocation ?
        'Error: The Geolocation service failed.' :
        'Error: Your browser doesn\'t support geolocation.');
}
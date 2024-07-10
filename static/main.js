window.initMap = function(){
    
    const coords = {lat: 16.908650978520416, lng: -92.09130381420194}

    const map = new google.maps.Map(document.getElementById("map"),{
        zoom:19,
        center:coords,
    });
    const marker = new google.maps.Marker({
        position: coords,
        map,
    })
}


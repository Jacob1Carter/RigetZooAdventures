function initMap() {
    console.log("here")
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 17,
        center: position,
        mapId: "RZA_MAP",
    });

    const marker = new google.marker.Marker({
        map: map,
        position: position,
        title: "Riget Zoo Adventures",
    });
    console.log("done");
}
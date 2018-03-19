
var dataBar = document.getElementById("data_bar")
var map = L.map('map',{zoomControl:false}).setView([mapLat, mapLong], mapZoom );
var mapToken = 'pk.eyJ1IjoibXBhdWxlZW4iLCJhIjoiY2pkOWFkM3dtNXJpdTJ4bjJnenU0djBicyJ9.S3X2k6KGLO1hlEBZukc-xw'

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    accessToken: mapToken,
	maxZoom: 18,
    id: 'mapbox.dark',
	attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
	'<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
	'Imagery © <a href="http://mapbox.com">Mapbox</a>'
}).addTo(map);

//Pin Color Settings
var geojsonMarkerOptions = {
	radius: 5,
	fillColor: "#45bef2", 
	color: "#000",
	weight: 1,
	opacity: 1,
	fillOpacity: 0.8
};

//Add Popup Info
function onEachFeature(feature, layer) {
	// does this feature have a property named popupContent?
	if (feature.properties && feature.properties.ID) {
		var str = ''+feature.properties.ID;
		layer.bindPopup(str,{offset:new L.Point(0,0)});
        console.log(str)
	}
}

function postOnClick(e){
    var stationId = e.target.feature.properties.ID;
    var address = e.target.feature.properties.Address;
    var lng = map.getCenter().lng
    var lat = map.getCenter().lat
    var zoom = map.getZoom()
    window.location = "/get_predict?station="+stationId+"&lng="+lng+"&lat="+lat+"&zoom="+zoom;
 

//    $("#data_bar").html(' \
//		<div> \
//		<!-- Default panel contents --> \
//		<div class= "data-header"> \
//		<div id="data-header">Station '+stationId +' selected </div>\
//		<div class="subtitle">Location: '+address +'</div>\
//		</div>\
//')
    
};  
L.geoJson(sites,
	{
        onEachFeature: onEachFeature,
		pointToLayer: function (feature, latlng) {
			console.log("mapping yo");
			var marker = L.circleMarker(latlng, geojsonMarkerOptions);
			marker.on('click', function(e){
                postOnClick(e);
			}); 
			return marker;

		},
    

	}).addTo(map);
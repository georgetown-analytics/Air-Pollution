var IDBLabHQ = {lat: 38.89943694195807, lng: -77.03052163124086};

var map = L.map('map',{
  zoomControl: false
}).setView(IDBLabHQ,10);

var mapLink =
	'<a href="http://openstreetmap.org">OSM</a> | <a href="https://github.com/georgetown-analytics/Air-Pollution">GTU</a> | <a href="https://github.com/collaer">code</a>';
var baseMap = L.tileLayer(
	'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	attribution: '&copy; ' + mapLink + ' ',
	maxZoom: 18,
	});

baseMap.addTo(map);

var myDecisionTreeClassifier;

var countriesLayer;

var COUTRIES_GEOJSON = (window.location.href.indexOf("file:")==-1 || true ?
"https://collaer.github.io/simplemap/data/LAC-countries.geojson"
:
"./DATA/countries2.geojson");




$(document).ready(function () {
	$('#loadedAlert').hide();

  myDecisionTreeClassifier = new DecisionTreeClassifier();

    $('#sidebarCollapse').on('click', function () {
        $('#sidebar, #content').toggleClass('active');
		setTimeout(function(){ map.invalidateSize()}, 400);
    });


	$(function () {
	  $('[data-toggle="popover"]').popover();
	});

	$(function () {
		$('[data-toggle="tooltip"]').tooltip()
	});

	$('#exampleModalCenter').on('show.bs.modal', function (e) {

		$('#datatable').bootstrapTable(
			'load', mydatatablejson
		);

	});


	$('.alert .close').on('click', function(e) {
		$(this).parent().hide();
	});


  countriesLayer = new L.GeoJSON.AJAX(COUTRIES_GEOJSON);
  countriesLayer.addTo(map);

  map.on('click', function(e) {
      var popLocation= e.latlng;
      contenHTML = '<h3>Forecast Air Quality at click position</h3>';
      contenHTML = contenHTML + "<ul>";

      var tomorrow = new Date();
      tomorrow.setDate(new Date().getDate()+1);
      var dayoftheweek = tomorrow.getDay();
      var sinday = -0.866025; //4pm
      var cosday = -0.500000; //4pm
      var now = new Date();
      var start = new Date(now.getFullYear(), 0, 0);
      var diff = now - start;
      var oneDay = 1000 * 60 * 60 * 24;
      var day_numb = Math.floor(diff / oneDay);
      var cos_year = Math.cos(2*Math.PI*day_numb/365);
      var sin_year = Math.sin(2*Math.PI*day_numb/365);

      var feature = [popLocation.lat, popLocation.lng, dayoftheweek, sinday, cosday, sin_year, cos_year, 20, -0.342020, 9.396926e-01, 4.6, 3.95, 1524.0, 1021.95]
      polluted = myDecisionTreeClassifier.predict(feature);
      contenHTML = contenHTML + "<li>At position (Lat " + popLocation.lat + ', Lng '  + popLocation.lng +  ")</li>";
      contenHTML = contenHTML + "<li>For tomorrow (day number "+dayoftheweek+" in the week and " + day_numb +  " in the year) at 4 PM</li>";
      contenHTML = contenHTML + "<li>With standard weather paramaters NOT PREDICTED (@todo use weather API) </li>";
      contenHTML = contenHTML + "</ul>";
      contenHTML = contenHTML + "<h3>Tomorrow at 4pm here, air Quality will be <b>" + (polluted ? ' Not Good':'Good') + "</b> [using EAP AQI taxonomy and model with 0.5 recall <a href='https://github.com/georgetown-analytics/Air-Pollution'>here</a>]</dh3>";
      var popup = L.popup({
        maxWidth: "auto"
      })
      .setLatLng(popLocation)
      .setContent(contenHTML)
      .openOn(map);
  });

});




// map.flyToBounds(Markers.getBounds(), {maxZoom:6});

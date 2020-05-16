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
      contenHTML = '<h3>Forecasted Air Quality for tomorrow</h3>';
      contenHTML = contenHTML + "<ul>";

      var tomorrow = new Date();
      tomorrow.setDate(new Date().getDate()+1);
      var dayoftheweek = tomorrow.getDay();
      var hour24 = parseFloat($("#hour24").val());
      var sinday = Math.sin(2*Math.PI*hour24/24.0);
      var cosday = Math.cos(2*Math.PI*hour24/24.0);

      var now = new Date();
      var start = new Date(now.getFullYear(), 0, 0);
      var diff = now - start;
      var oneDay = 1000 * 60 * 60 * 24;
      var day_numb = Math.floor(diff / oneDay);
      var cos_year = Math.cos(2*Math.PI*day_numb/365);
      var sin_year = Math.sin(2*Math.PI*day_numb/365);

      var feature = [popLocation.lat, popLocation.lng, dayoftheweek,
        sinday, cosday, sin_year, cos_year,
        parseFloat($("#temp").val()),
        parseFloat($("#cos_wind").val()),
        parseFloat($("#sin_wind").val()),
        parseFloat($("#wind").val()),
        parseFloat($("#DEW").val()),
        parseFloat($("#SKY").val()),
        parseFloat($("#ATM").val())]

      polluted = myDecisionTreeClassifier.predict(feature);
      contenHTML = contenHTML + "<li>At position (Lat " + popLocation.lat + ', Lng '  + popLocation.lng +  ")</li>";
      contenHTML = contenHTML + "<li>Tomorrow (day weeknumber "+dayoftheweek+" and " + day_numb +  " year number) at " + hour24 + " hour.</li>";
      contenHTML = contenHTML + "<li>Using weather paramaters from your form (@todo use weather API service) </li>";
      contenHTML = contenHTML + "</ul>";
      contenHTML = contenHTML + '<div class="alert alert-' + (polluted?"danger":"success") + '" role="alert">Our model predict air Quality to be <b>' + (polluted ? "BAD":"GOOD");
      contenHTML = contenHTML + '</b> using EPA AQI and DecisionTreeClassifier model with 0.5 recall of predicting badweather. Check our <a style="color:black;text-decoration:underline;" href="https://github.com/georgetown-analytics/Air-Pollution">code</a> for more detail or to improve it.</div>';
      var popup = L.popup({
        maxWidth: "auto"
      })
      .setLatLng(popLocation)
      .setContent(contenHTML)
      .openOn(map);
  });

});




// map.flyToBounds(Markers.getBounds(), {maxZoom:6});

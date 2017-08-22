// Filter button function
+function ($) {
	'use strict';
		$(document).ready(function(){
			$(".filter-button").click(function(){
				var value = $(this).attr('data-filter');
				if(value == "all") {
					$('.filter').show('1000');
				} else {
					$(".filter").not('.' + value).hide('3000');
					$('.filter').filter('.' + value).show('3000');
				}
			});
		});
}(jQuery);

// Google maps function
function map_init(id) {     

	var var_map;
	var var_location = new google.maps.LatLng(45.430817,12.331516);

	var var_mapoptions = {
		center: var_location,
		zoom: 14,
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		mapTypeControl: false,
		panControl:false,
		rotateControl:false,
		streetViewControl: false,
	};
				
	var_map = new google.maps.Map(document.getElementById(id.concat("-map")), var_mapoptions);
						
	var contentString = 
		'<div id="mapInfo">'+
		'<p><strong>Peggy Guggenheim Collection</strong><br><br>'+
		'Dorsoduro, 701-704<br>' +
		'30123<br>Venezia<br>'+
		'P: (+39) 041 240 5411</p>'+
		'<a href="http://www.gffffm.org/venice" target="_blank">Plan your visit</a>'+
		'</div>';
		 
	var var_infowindow = new google.maps.InfoWindow({ 
			content: contentString 
	});
							
	var var_marker = new google.maps.Marker({
		position: var_location,
		map: var_map,
		title:"Click for information about the Guggenheim museum in Venice", maxWidth: 200, maxHeight: 200 
	});
		 
	google.maps.event.addListener(var_marker, 'click', function() {
		var_infowindow.open(var_map,var_marker);
	});

	google.maps.event.addDomListener(window, 'load', map_init);

	//start of modal google map
	$('#' + id).on('shown.bs.modal', function () {
		google.maps.event.trigger(var_map, "resize");
		var_map.setCenter(var_location);
	});
}

/* Function that sets the opacity of the posts to 1 while scrolling the webpage
   This will make the post divs appear fade in while scrolling.
   Opacity for the class ".fades" is  initially set to 0 */
+function ($) {
	'use strict';
		var width = (window.innerWidth > 0) ? window.innerWidth : document.documentElement.clientWidth;
			$(window).on("load",function() {
				$(window).scroll(function() {
					var windowBottom = $(this).scrollTop() + $(this).innerHeight() + 700;
					$(".fades").each(function() {
						/* Check the location of each desired element */
						var objectBottom = $(this).offset().top + $(this).outerHeight();
						if( windowBottom > objectBottom ){
							$(this).fadeTo(600,1);
						}
						/* If the element is completely within bounds of the window, fade it in 
						if (objectBottom < windowBottom) { //object comes into view (scrolling down)
							if ($(this).css("opacity")==0) {$(this).fadeTo(600,1);}
						} else { //object goes out of view (scrolling up)
							if ($(this).css("opacity")==1) {$(this).fadeTo(600,0);}
						}*/
					});
				}).scroll(); //invoke scroll-handler on page-load
			});
}(jQuery);

$(document).ready(function(){
    $('[data-toggle="popover"]').popover(); 
});

// Submit comment on submit
$('#comment-form').on('submit', function(event){
	event.preventDefault();
	add_comment();
});
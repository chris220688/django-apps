// AJAX code for for adding a like
function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Function that adds a like using an ajax request
function like_post(post_id) {
	// Get the CSRF token from the "csrftoken" cookie
	// We will need to pass it as an argument to the POST request
	var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

	$.ajax({
		// We should always perform this when we make an ajax request
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		},
		// URL endpoint. This will actually look like:
		// /blog/like_post/
		url : "like_post/",
		type : "POST",
		// data dictionary sent with the post request
		data : { 
			'post_id' : post_id
		},

		// handle a successful response
		success : function(json) {
			// If we have successfuly added the like in the DB, we need
			// to change the colour of the button and disable it
			$("#likes-btn-" + post_id + " span").css('color', '#cecbcb');
			$("#likes-btn-" + post_id).attr("disabled", true);
			// Also update the number of likes
			$("#likes-nbr-" + post_id + " a").text("Likes " + json.likes_count);
		},

		// handle a non-successful response
		error : function(xhr,errmsg,err) {
			// add the error to the DOM
			$('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
				" <a href='#' class='close'>&times;</a></div>");
			// provide a bit more info about the error to the console
			console.log(xhr.status + ": " + xhr.responseText);
		}
	});
};
// Event handler when the submit button in the comments section is pressed
$('#comment-form').on('submit', function(event){
	// Prevent from submitting the form
	event.preventDefault();
	if ($('#id_text').val()) {
		// Call add_comment() below
		add_comment();
	}
});

// AJAX code for for adding a comment
function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// Function that adds a comment using an ajax request
// 1. Calls "post" view using ajax
// 2. Takes a json response from the "post" view
// 3. Removes the text from the textfield
// 4. Adds the comment (returned in json) to the DOM
// 5. Throws error in case of failure
function add_comment() {
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
		// /blog/post-12/add_comment/
		type : "POST",
		// data dictionary sent with the post request
		// The data names should be same as the default
		// django is using in teh forms
		data : { 
			text : $('#id_text').val(),
			post : $('#id_post').val()
		},

		// handle a successful response
		success : function(json) {
			// remove the value from the input textfield
			$("#id_text").val('');
			// Append the comment at the end of the list of comments in the DOM
			$("#comments-list").append("                                        \
					<li>                                                        \
						<div class='commenterImage'>                            \
							<img src='/media/" + json.commenter_image + "'/>    \
						</div>                                                  \
						<div class='commentText'>                               \
							<p class=''>" + json.text + "</p>                   \
						</div>                                                  \
						<span class='date sub-text'>on " + json.date + "</span> \
					</li>                                                       \
			");
			// Increment the comments number
			$("#comments-count a").text('Comments ' + json.comments_count);
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

from django.http      import HttpResponse, Http404
from django.shortcuts import render
from blog.models      import (
	tPost,
	tComment,
	tLike
)
from django.contrib.auth.models import User
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.html import escape
from blog.forms import CommentForm
import datetime

# View that returns all the posts, ordered by date, in blog.html
# URL: /blog
#
# Arguments: -request
# Returns:   all the posts ordered by date
def blog(request):

	all_posts = tPost.objects.all().order_by('-date')

	# Show 2 posts per page
	paginator = Paginator(all_posts, 2)

	# Get the page number passed by the request
	page = request.GET.get('page')

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		posts = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		posts = paginator.page(paginator.num_pages)

	liked_posts = {}

	# If the user is logged in, get the post_ids of the posts he has liked
	if request.user.is_authenticated():
		liked_posts = tLike.objects.all().filter(user_id=request.user).values_list('post', flat=True)

	template = 'blog/blog.html'
	# We will also need to get a count of all comments for each post
	# To do this we will use django's "RelatedManager" in blog.html
	# which will give us a backwards relationship from tComment to tPost.
	# See _set.all() function. i.e {{ post.tcomment_set.all.count }}
	context = {
		'posts' : posts,
		'liked_posts' : liked_posts,
		'page_range' : paginator.page_range,
	}
	return render(request, template, context)

# View that returns a specific post
# URL: /blog/post-12
#
# Arguments: -request
#            -post_id
# Returns:   context dictionary with the post and all of its comments
def post(request, post_id):
	# If the request is POST it means that it comes from an ajax request in post.js
	if request.method == 'POST':
		# Create a CommentForm instance.
		# Beware!!! CommentForm needs to be an instance of tComment table, so that we
		# can use the save() method to save it in the DB. Since tComment has a foreign
		# key to user_auth table, we need to pass it a user_auth instance for the user
		# that called the function. This will add the user_id for us in the table.
		comment_form = CommentForm(request.POST, instance=tComment(user=request.user))

		if comment_form.is_valid():

			comment_form.save()

			# Create the repsonse data to return to the add_comment() in post.js
			response_data = {}
			response_data['text'] = escape(comment_form.cleaned_data['text'])
			# Add the url of the commenters avatar
			response_data['commenter_image'] = str(request.user.tuserprofile.avatar)
			# Find the new total number of comments for this post
			response_data['comments_count'] = tComment.objects.all().filter(post=post_id).count()
			# Cast date to a string and make the format look like the one django template is using
			# Django template:   July 3, 2017, 7:17 p.m.
			# strftime function: July 3, 2017, 7:17 PM.
			# Needs to be fixed
			response_data['date'] = str(datetime.datetime.now())

			return HttpResponse(
				json.dumps(response_data),
				content_type="application/json"
			)

		else:
			return HttpResponse('<h4>Invalid form</h4>')
	# If the request is GET
	else:
		post = tPost.objects.all().filter(id=post_id).first()
		all_comments = tComment.objects.all().filter(post=post_id).order_by('date')
		
		# Get all the users that liked this post
		# We will need users objects so that we can read the username. i.e user.username
		# Filtering the tLikes table will not do, as we can only retrieve the ids of the users
		# The following would be like:
		# Select * from user_auth where id in (select user from tLike where post = post_id)
		# The __ helps querying across relationships
		users_liked = User.objects.all().filter(tlike__post=post_id)

		# If the user is authenticated, we need to find out whether he has already liked this post
		post_liked = False

		if request.user.is_authenticated():
			if tLike.objects.all().filter(user_id=request.user, post=post.id):
				post_liked = True

		template = "blog/post.html"

		# Prepopulate the hidden input with the id of the post
		# Forms take a dictionary as argument
		comment_form = CommentForm({'post': post_id})

		context = {
			'post':         post,
			'all_comments': all_comments,
			'users_liked':  users_liked,
			'post_liked':   post_liked,
			'comment_form': comment_form,
		}
		return render(request, template, context)

# Function that adds a like in tLike table
def like_post(request):
	if request.method == 'POST':

		post_id = request.POST.get('post_id')

		response_data = {}

		like = tLike(user=request.user, post=tPost.objects.get(id=post_id))

		# Do a sanity check in case for some reason the user has already liked this post
		if not tLike.objects.all().filter(user=request.user, post=post_id):
			like.save()

		# We need to return the new likes count to update it in the template
		response_data['likes_count'] = tLike.objects.all().filter(post=post_id).count()

		return HttpResponse(
			json.dumps(response_data),
			content_type="application/json"
		)

	else:
		return HttpResponse(
			json.dumps({"nothing to see": "this isn't happening"}),
			content_type="application/json"
		)
		
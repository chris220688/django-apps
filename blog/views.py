# Standard library imports
import datetime
import json

# Django imports
from django.contrib.auth.models import User
from django.core.paginator import (
    Paginator, EmptyPage, PageNotAnInteger
)
from django.http import (
    HttpResponse, Http404
)
from django.shortcuts import render
from django.utils.html import escape

# Local Django imports
from blog.forms import CommentForm
from blog.models import (
    tPost, tComment, tLike
)


def blog(request):
    """ Handle a GET request to /blog.

        Args:
            request: A GET HttpRequest to /blog

        Returns:
            An HttpResponse object with all the posts ordered by date
    """

    template = 'blog/blog.html'
    all_posts = tPost.objects.all().order_by('-date')
    liked_posts = {}
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

    # If the user is logged in, get the post_ids of the posts he has liked
    if request.user.is_authenticated():
        liked_posts = tLike.objects.all().filter(user_id=request.user).values_list('post', flat=True)

    context = {
        'posts': posts,
        'liked_posts': liked_posts,
        'page_range': paginator.page_range,
    }

    return render(request, template, context)

def post(request, post_id):
    """ Handle a request to /blog/post-<id>.

        Args:
            request: An HttpRequest to /blog/post-<id>
            post_id: The id of the post

        Returns:
            An HttpResponse object with the post and all of its comments

        Raises:
            Http404
                When the post does not exists
    """

    # POST request: It originates from an ajax request by post.js
    if request.method == 'POST':
        """
        Create a CommentForm instance.
        Beware!!! CommentForm needs to be an instance of tComment table,
        so that we can use the save() method to save it in the DB. Since
        tComment has a foreign key to user_auth table, we need to pass it
        a user_auth instance for the user that called the function.
        This will add the user_id for us in the table.
        """
        comment_form = CommentForm(request.POST, instance=tComment(user=request.user))

        if comment_form.is_valid():
            comment_form.save()
            # Create the repsonse data to return to add_comment() in post.js
            response_data = {}
            response_data['text'] = escape(comment_form.cleaned_data['text'])
            # Add the url of the commenters avatar
            response_data['commenter_image'] = str(request.user.tuserprofile.avatar)
            # Find the new total number of comments for this post
            response_data['comments_count'] = tComment.objects.all().filter(post=post_id).count()

            """
            Cast date to a string and make the format look like the one
            django template is using. Needs to be fixed.
            Example:
            Django template:   July 3, 2017, 7:17 p.m.
            strftime function: July 3, 2017, 7:17 PM.
            """
            response_data['date'] = str(datetime.datetime.now())

            return HttpResponse(
                json.dumps(response_data),
                content_type='application/json'
            )
        else:
            return HttpResponse('<h4>Invalid form</h4>')
    # GET request
    else:
        try:
            post = tPost.objects.get(pk=post_id)
        except tPost.DoesNotExist:
            raise Http404('Post does not exist')

        template = 'blog/post.html'
        all_comments = tComment.objects.all().filter(post=post_id).order_by('date')
        
        """
        Get all the users that liked this post. We need users objects so that
        we can read the username. i.e user.username
        Filtering the tLikes table will not do, as we can only retrieve the
        ids of the users. The following would be like:
        Select * from user_auth where id in (
                select user from tLike where post = post_id
        )
        The __ helps querying across relationships
        """
        users_liked = User.objects.all().filter(tlike__post=post_id)

        # If the user is authenticated, find out if he already liked this post
        post_liked = False

        if request.user.is_authenticated():
            if tLike.objects.all().filter(user_id=request.user, post=post.id):
                post_liked = True

        # Prepopulate the hidden input with the id of the post
        comment_form = CommentForm({'post': post_id})

        context = {
            'post': post,
            'all_comments': all_comments,
            'users_liked': users_liked,
            'post_liked': post_liked,
            'comment_form': comment_form,
        }

        return render(request, template, context)

def like_post(request):
    """ Handle an ajax request for a liked post.

        Args:
            request: An ajax HttpRequest to /blog/post-<id>/like_post/

        Returns:
            An HttpResponse to like_post() javascript function
    """

    # POST request:
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        response_data = {}
        like = tLike(user=request.user, post=tPost.objects.get(id=post_id))

        # Do a sanity check in case the user has already liked this post
        if not tLike.objects.all().filter(user=request.user, post=post_id):
            like.save()

        # We need to return the new likes count to update it in the template
        response_data['likes_count'] = tLike.objects.all().filter(post=post_id).count()

        return HttpResponse(
            json.dumps(response_data),
            content_type='application/json'
        )

    else:
        return HttpResponse(
            json.dumps({'nothing to see': 'not happening'}),
            content_type='application/json'
        )
        
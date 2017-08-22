from django.conf.urls import url
import blog.views

urlpatterns = [
	# /blog/
    url(r'^$', blog.views.blog, name='blog'),
    # /blog/like_post/
    url(r'^like_post/$', blog.views.like_post , name='like_post'),
    # /blog/post-12/like_post/
	url(r'^post-[0-9]*/like_post/$', blog.views.like_post , name='like_post'),
    # /blog/post-12/
    url(r'^post-(?P<post_id>[0-9]+)/$', blog.views.post, name='post'),
    # /blog/post-12/add_comment/
    url(r'^post-(?P<post_id>[0-9]+)/add_comment/$', blog.views.add_comment, name='add_comment'),
]
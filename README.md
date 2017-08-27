# django-apps

Django Website
------

This is a project I have started working on a few months ago, on my quest to teach myself Python and Django.

The aim is to create a blog that will focus on the homelessness crisis in the UK. The blog will also allow registered users to obtain vouchers for several products.

There is also a chance for an additional feature to make donations in the local holmeless communities.

Visit [this link](https://chris220688.github.io/blog.html) to see a demo of the website.

#### Technologies

1. Python, Django
2. Javascript, JQuery
3. CSS, Bootstrap
4. PostgreSQL

Todo list
------

#### Bugs
1. Likes modal in post.html is not updated when a user likes the post (needs ajax change)
2. Fix json error functions in post.js, blog.js
3. Date string that returns from add_comment view (through json) needs to have same format as the django template. (p.m instead of PM)
4. When clicking the back button the page is not updated until you physically refresh it. (i.e go to a post page, like the post, move back to the blog page)
5. CSRF token cookie is not deleted after account/logout

#### Account Features
1. Forgot/Reset my password (To be implemented using the inbuilt Django library + email notification)
2. Deleting or de-activating accounts?

#### Other Features
1. Enable email notifications when users subscribe to Newsletter
2. Add default user images
3. Search post functionality
3. Allow basic html elements in text inputs from the admin screens (In a secure way!!!)

#### User experience
1. Create a proper response for invalid logins
2. Exceptions and Http 404 where content doesn’t exist. (i.e if we hit the url /blog/post-2222/ but post 2222 doesn’t exist)
3. Consider using slugs

#### Security
1. Go full HTTPS
2. Specific URLs should be restricted. (i.e logged in users should not be able to access the registration page)
3. Throttling of login attempts
4. Password strength checking
5. Add some sort of security in manage.py script. Not everyone should be able to run it

#### House keeping
1. When a new image is uploaded in /media directory, remove the old one
2. CDN fallback to local CSS and JS files
3. Consider ansible playbooks for the deployment
4. LOGS!

#### Pre-Live checks
1. Fix STATICS and MEDIA directories for production
2. Turn off DEBUG for production!

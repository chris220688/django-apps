# Django imports
from django.contrib import admin

# Local Django imports
from .models import tPost


class ModelAdmin(admin.ModelAdmin):
    """ Override the default admin model functions """

    """
    Exclude the author field.
    The author will be populated automatically.
    This way a user will not be able to select a name other
    than his when adding a post in the admin screens
    """
    exclude = ('author', 'date')

    # List the fields that we want to appear in the admin screens 
    list_display = ('title', 'author', 'date')

    def has_change_permission(self, request, obj=None):
        """ Identify whether a user has permissions to modify a post

            Args:
                request: A HttpRequest to change a post
                obj: The object. Defaults to None

            Returns:
                True:  If the user has permissions
                False: If the user does not have permissions
        """

        has_class_permission = super(ModelAdmin, self).has_change_permission(request, obj)

        if not has_class_permission:
            return False

        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False

        return True

    def get_queryset(self, request):
        """ Handle post visibility.
            If the user is not the administrator, show only his posts

            Args:
                request: The HttpRequest to get the posts

            Returns:
                A number of post objects according to the user
        """

        if request.user.is_superuser:
            return tPost.objects.all().order_by('-date')

        return tPost.objects.filter(author=request.user).order_by('-date')

    def save_model(self, request, obj, form, change):
        """ Populate the "author" field programmaticaly.
            The "author" will take the value of the user who is logged
            in at the time he is adding a post

            Args:
                request: The HttpRequest
                obj: A model instance
                form: A ModelForm instance
                change: A boolean value based on whether the object
                        is added or changed
        """
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(tPost, ModelAdmin)


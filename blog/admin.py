from django.contrib import admin
from .models import tPost

# Override the default admin model functions
class ModelAdmin(admin.ModelAdmin):
    # Exclude the author field.
    # The author will be populated automatically.
    # This way a user will not be able to select a name other
    # than his when adding a post in the admin screens
    exclude = ('author', 'date')

    # List the fields that we want to appear in the admin screens 
    list_display = ('title', 'author', 'date')

    # Only allow a user to modify a post if he has change permissions
    def has_change_permission(self, request, obj=None):
        has_class_permission = super(ModelAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.author.id:
            return False
        return True

    # If the user is not the administrator, show only his posts
    def get_queryset(self, request):
        if request.user.is_superuser:
            return tPost.objects.all().order_by('-date')
        return tPost.objects.filter(author=request.user).order_by('-date')

    # Populate the "author" field programmaticaly
    # The "author" will take the value of the user who is logged in
    # at the time he is adding a post
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        obj.save()

admin.site.register(tPost, ModelAdmin)
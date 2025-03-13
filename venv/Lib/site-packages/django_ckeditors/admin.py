"""django-ckeditors Admin file."""

from django.contrib import admin

from .models import UnusedImageURLS

# Register your tag_me models here.

admin.site.register(UnusedImageURLS)

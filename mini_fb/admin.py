## Register the models with the Django Admin tool
from django.contrib import admin

from .models import *
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(Friends)
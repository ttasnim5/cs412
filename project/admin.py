from django.contrib import admin

from .models import *
admin.site.register(Cause)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(NutritionalInfo)
admin.site.register(EnvironmentalInfo)

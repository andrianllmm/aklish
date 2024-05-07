from django.contrib import admin
from .models import Profile, LoginSession


admin.site.register(Profile)
admin.site.register(LoginSession)
from django.contrib import admin
from .models import User, Post, Like, Follow

admin.site.register([User, Post, Like, Follow])


from django.contrib import admin
from .models import User, Follower, Comment, Post

# Register your models here.
admin.site.register(User)
admin.site.register(Follower)
admin.site.register(Comment)
admin.site.register(Post)
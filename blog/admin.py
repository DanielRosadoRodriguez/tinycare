from django.contrib import admin
from .models.blog_model import Blog
from .models.comment_model import Comment
# Register your models here.
admin.site.register(Blog)
admin.site.register(Comment)
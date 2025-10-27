from django.db import models
from .blog_model import Blog
from django.contrib.auth.models import User

class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE
    )
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f'Comentario de {self.author.username} el {self.blog.title}'
    
    @property
    def is_parent(self):
        return self.parent is None
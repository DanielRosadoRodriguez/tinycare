from django.urls import reverse
from ..models.comment_model import Comment
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'comment/comment_form.html'
    fields = ['content']
    
    def get_success_url(self):
        return reverse('blogs:blog-detail', kwargs={'pk': self.object.blog.pk})

class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'comment/comment_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('blogs:blog-detail', kwargs={'pk': self.object.blog.pk})
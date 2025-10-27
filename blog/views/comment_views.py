from ..models.comment_model import Comment
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
    
class CommentCreateView(CreateView):
    model = Comment
    template_name = 'blog/blog_detail.html'
    fields = ['blog', 'content']
    success_url = '/comments/'

class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'blog/comment_form.html'
    fields = ['content']
    success_url = '/comments/'

class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    success_url = '/comments/'
    

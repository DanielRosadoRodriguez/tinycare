from django.urls import reverse
from ..models.comment_model import Comment
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from ..permissions.owner_permission_mixin import OwnerPermissionMixin

class CommentUpdateView(OwnerPermissionMixin, UpdateView):
    permission_required = 'blog.change_comment'
    model = Comment
    template_name = 'comment/comment_form.html'
    fields = ['content']
    
    def get_success_url(self):
        return reverse('blogs:blog-detail', kwargs={'pk': self.object.blog.pk})

class CommentDeleteView(OwnerPermissionMixin, DeleteView):
    permission_required = 'blog.delete_comment'
    model = Comment
    template_name = 'comment/comment_confirm_delete.html'
    
    def get_success_url(self):
        return reverse('blogs:blog-detail', kwargs={'pk': self.object.blog.pk})
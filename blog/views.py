from django.shortcuts import redirect, render
from .models import Blog
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import markdown

class LogginRequiredMixin:
    """Mixin to ensure the user is logged in."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:register')
        return super().dispatch(request, *args, **kwargs)

class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 10
    
class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'].content = markdown.markdown(context['blog'].content, extensions=['fenced_code', 'codehilite'])
        return context
        
class BlogCreateView(CreateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content']
    success_url = '/blogs/'
    
class BlogUpdateView(UpdateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content']
    success_url = '/blogs/'

class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = '/blogs/'
    
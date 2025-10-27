from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ..models.blog_model import Blog

class BlogIndex(ListView):
    model = Blog
    template_name = 'blog/blog_index.html'
    context_object_name = 'blogs'
    paginate_by = 10
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.only('id', 'title', 'created_at').order_by('-created_at')
    
class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'
        
class BlogCreateView(CreateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content']
    success_url = '/blogs/'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        print("Blog created by:", form.instance.author)
        return super().form_valid(form)
    
class BlogUpdateView(UpdateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content']
    success_url = '/blogs/'

class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = '/blogs/'
    
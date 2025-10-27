from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ..models.blog_model import Blog
from ..forms.comment_form import CommentForm

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.order_by('-created_at')
        context['form'] = kwargs.get('form', CommentForm())
        return context
    
    def post(self, request, *args, **kwargs):
        # Obtenemos el blog actual
        self.object = self.get_object()
        form = CommentForm(request.POST)
        form.instance.author = request.user
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = self.object
            comment.save()
            return redirect('blogs:blog-detail', pk=self.object.pk)

        # Si el formulario tiene errores, los mostramos
        context = self.get_context_data(form=form)
        return self.render_to_response(context)

class BlogCreateView(CreateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content']
    success_url = '/blogs/'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
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
    
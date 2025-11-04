from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from accounts.models.profile_parent import ProfileParent
from accounts.models.profile_specialist import ProfileSpecialist
from notifications.models import Notification
from ..models.blog_model import Blog
from ..forms.comment_form import CommentForm
from accounts.permissions.specialit_comment_permission import is_specialit
from accounts.permissions.owner_permission_mixin import OwnerPermissionMixin
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
class BlogIndex(ListView):
    model = Blog
    template_name = 'blog/blog_index.html'
    context_object_name = 'blogs'
    paginate_by = 10
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.only('id', 'title', 'created_at', 'author').order_by('-created_at')
     
class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.order_by('-created_at')
        if is_specialit(self.request.user):
            context['form'] = kwargs.get('form', CommentForm())
        return context
    
    @method_decorator(user_passes_test(is_specialit))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        form.instance.author = request.user
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = self.object
            comment.save()
            
            # --- INICIO DE LÓGICA DE NOTIFICACIÓN ---
            try:
                # 1. Obtener el autor del blog (que es un User)
                blog_author_user = self.object.author
                
                # 2. Encontrar el perfil de Padre de ese User
                parent_to_notify = ProfileParent.objects.filter(user=blog_author_user).first()
                
                # 3. Obtener el perfil del especialista que comenta
                specialist_profile = ProfileSpecialist.objects.get(user=request.user)
                specialist_name = f"{specialist_profile.nombres} {specialist_profile.apellido_paterno}".strip()

                # 4. Solo notificar si el autor del blog es un Padre
                if parent_to_notify:
                    # 5. Crear el mensaje
                    message = (
                        f"El especialista {specialist_name} ha respondido "
                        f"a tu publicación: {self.object.title}."
                    )
                    
                    # 6. Crear la notificación
                    Notification.objects.create(
                        user=parent_to_notify,
                        message=message,
                        notification_type=Notification.COMMENT,
                        content_object=comment  # Enlaza la notificación al comentario
                    )
            except Exception as e:
                # Opcional: registrar el error si la notificación falla
                print(f"Error al crear notificación de comentario: {e}")
            # --- FIN DE LÓGICA DE NOTIFICACIÓN ---

            return redirect('blogs:blog-detail', pk=self.object.pk)

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
    
class BlogUpdateView(OwnerPermissionMixin, UpdateView):
    permission_required = 'blog.change_blog'
    model = Blog
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content']
    success_url = '/blogs/'

class BlogDeleteView(OwnerPermissionMixin, DeleteView):
    permission_required = 'blog.delete_blog'
    model = Blog
    template_name = 'blog/blog_confirm_delete.html'
    success_url = '/blogs/'
    
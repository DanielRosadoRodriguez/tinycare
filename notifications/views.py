from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from .models import Notification
from accounts.models.profile_parent import ProfileParent

class NotificationListView(LoginRequiredMixin, ListView):
    """
    Muestra una página con todas las notificaciones (leídas y no leídas)
    para el padre/madre que está logueado.
    """
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20  # Paginación

    def get_queryset(self):
        try:
            # 1. Obtener el perfil del padre logueado
            parent_profile = ProfileParent.objects.get(user=self.request.user)
        except ProfileParent.DoesNotExist:
            # Si no es un padre (ej. un especialista), no tiene notificaciones
            return Notification.objects.none()
        
        # 2. Devolver todas las notificaciones para ESE padre
        # Ordenadas por "no leídas" primero, y luego por fecha
        return Notification.objects.filter(user=parent_profile).order_by('is_read', '-created_at')

    def get_context_data(self, **kwargs):
        """
        Separa las notificaciones en dos grupos (no leídas y leídas)
        para mostrarlas fácilmente en el template.
        """
        
        # --- INICIO DE LA CORRECCIÓN ---
        
        # 'self.object_list' contiene el queryset COMPLETO (sin paginar)
        # que fue definido en get_queryset().
        # Usamos este para nuestros filtros.
        full_queryset = self.object_list
        
        # Obtenemos el contexto del padre (que incluye la paginación)
        context = super().get_context_data(**kwargs)
        
        # Agregamos nuestras listas filtradas (del queryset completo) al contexto
        context['unread_notifications'] = full_queryset.filter(is_read=False)
        context['read_notifications'] = full_queryset.filter(is_read=True)
        
        # --- FIN DE LA CORRECCIÓN ---
        
        return context

class NotificationDetailView(LoginRequiredMixin, DetailView):
    """
    Muestra una notificación específica.
    Al cargar esta vista, la notificación se marca automáticamente como leída.
    """
    model = Notification
    template_name = 'notifications/notification_detail.html'
    context_object_name = 'notification'

    def get_queryset(self):
        """
        Sobrescribimos esto por seguridad:
        Un usuario SOLO puede ver sus propias notificaciones.
        """
        try:
            parent_profile = ProfileParent.objects.get(user=self.request.user)
            return Notification.objects.filter(user=parent_profile)
        except ProfileParent.DoesNotExist:
            # Si no es un padre, no puede ver ninguna notificación
            raise Http404("Perfil no encontrado")

    def get_object(self, *args, **kwargs):
        """
        Cuando se obtiene el objeto (la notificación),
        la marcamos como leída.
        """
        obj = super().get_object(*args, **kwargs)
        
        # Marcarla como leída
        if not obj.is_read:
            obj.is_read = True
            obj.save(update_fields=['is_read'])
        
        return obj
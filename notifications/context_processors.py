from .models import Notification
from accounts.models import ProfileParent

def unread_notification_count(request):
    """
    Agrega el conteo de notificaciones no leídas al contexto
    de todas las plantillas.
    """
    if not request.user.is_authenticated:
        return {'unread_notification_count': 0}
    
    try:
        # Busca el perfil de padre del usuario logueado
        parent_profile = ProfileParent.objects.get(user=request.user)
        count = Notification.objects.filter(user=parent_profile, is_read=False).count()
        return {'unread_notification_count': count}
    except ProfileParent.DoesNotExist:
        # El usuario está logueado pero no es un padre (es especialista)
        return {'unread_notification_count': 0}
import threading
from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
    def ready(self):
        from notifications.tasks import run_daily_reminders
        import sys
        if 'runserver' in sys.argv:
            hilo = threading.Thread(
                target=run_daily_reminders,
                args=(15, 41),  # Ejecutar a las 08:00 AM
                daemon=True
            )
            hilo.start()
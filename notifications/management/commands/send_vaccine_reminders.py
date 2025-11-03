import datetime
from django.core.management.base import BaseCommand
# ¡IMPORTANTE! Añade esta línea
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from vaccines.models.vaccine import Vaccine

class Command(BaseCommand):
    help = 'Envía recordatorios de vacunas pendientes.'

    def handle(self, *args, **options):
        today = datetime.date.today()
        three_days_later = today + datetime.timedelta(days=3)
        
        self.stdout.write(f"Buscando recordatorios para {today} y {three_days_later}...")

        # --- Trigger: Vacunas en 3 días ---
        vaccines_3_days = Vaccine.objects.filter(
            status=Vaccine.PENDING,
            applied_at=three_days_later
        )
        
        # Optimizacion: Obtenemos el ContentType de Vaccine una sola vez
        try:
            vaccine_content_type = ContentType.objects.get_for_model(Vaccine)
        except ContentType.DoesNotExist:
            self.stderr.write(self.style.ERROR('El modelo Vaccine no tiene un ContentType. Ejecuta migraciones.'))
            return

        for vaccine in vaccines_3_days:
            parent_to_notify = vaccine.baby.parent
            message = (
                f"Recordatorio: La vacuna {vaccine.name} para "
                f"{vaccine.baby.nombre} está programada en 3 días "
                f"({three_days_later.strftime('%d/%m/%Y')})."
            )
            
            # --- INICIO DE CORRECCIÓN ---
            # Usamos get_or_create con las columnas de BD correctas
            notif, created = Notification.objects.get_or_create(
                user=parent_to_notify,
                notification_type=Notification.VACCINE_3_DAYS,
                content_type=vaccine_content_type,  # Columna 1
                object_id=vaccine.pk,               # Columna 2
                defaults={'message': message}
            )
            # --- FIN DE CORRECCIÓN ---

            if created:
                self.stdout.write(f"Notificación de 3 días CREADA para {parent_to_notify.user.email}")

        # --- Trigger: Vacunas para Hoy ---
        vaccines_today = Vaccine.objects.filter(
            status=Vaccine.PENDING,
            applied_at=today
        )
        
        for vaccine in vaccines_today:
            parent_to_notify = vaccine.baby.parent
            message = (
                f"¡Hoy es el día! La vacuna {vaccine.name} para "
                f"{vaccine.baby.nombre} está programada para hoy "
                f"({today.strftime('%d/%m/%Y')})."
            )
            
            # --- INICIO DE CORRECCIÓN ---
            notif, created = Notification.objects.get_or_create(
                user=parent_to_notify,
                notification_type=Notification.VACCINE_TODAY,
                content_type=vaccine_content_type,  # Columna 1
                object_id=vaccine.pk,               # Columna 2
                defaults={'message': message}
            )
            # --- FIN DE CORRECCIÓN ---

            if created:
                self.stdout.write(f"Notificación de HOY CREADA para {parent_to_notify.user.email}")

        self.stdout.write(self.style.SUCCESS('Proceso de recordatorios finalizado.'))
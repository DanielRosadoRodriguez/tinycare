import threading
import time
from datetime import timedelta
from django.utils import timezone
from django.core.management import call_command


def wait_until_next_execution(target_hour, target_minute):
    """Returns the seconds until the next scheduled time."""
    now = timezone.localtime()
    next_run = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
    if next_run <= now:
        next_run += timedelta(days=1)
    return (next_run - now).total_seconds()


def run_daily_reminders(hour, minute):
    """Runs the 'send_reminders' command once a day at the specified time."""
    while True:
        seconds = wait_until_next_execution(hour, minute)
        print(f"[{timezone.now()}] Waiting {seconds/3600:.2f} hours to send reminders...")
        time.sleep(seconds)

        print(f"[{timezone.now()}] Running command 'send_reminders'...")
        # Assuming 'enviar_recordatorios' command name is also translated
        call_command('send_vaccine_reminders')  # 👈 executes your Command 
        print(f"[{timezone.now()}] Command completed. Waiting 24 hours...")
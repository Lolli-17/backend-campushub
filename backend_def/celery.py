import os
from celery import Celery
from celery.schedules import crontab

# Imposta la variabile d'ambiente per le impostazioni di Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_def.settings')

app = Celery('backend_def')

# Usa le impostazioni di Django per configurare Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carica automaticamente i file tasks.py da tutte le app registrate in Django
app.autodiscover_tasks()

# Definiamo la pianificazione (schedule) per i nostri task con Celery Beat
app.conf.beat_schedule = {
    'update-guest-nights-every-day': {
        'task': 'campus_management.tasks.update_guest_nights',
        # crontab(minute=5, hour=0) significa "esegui ogni giorno alle 00:05"
        'schedule': crontab(minute=5, hour=0), 
    },
    'activate-notifications-every-minute': {
        'task': 'campus_management.tasks.activate_scheduled_notifications',
        # Esegue il task ogni 60 secondi
        'schedule': 60.0,
    },
}
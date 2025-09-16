from django.core.management.base import BaseCommand
from django.utils import timezone
from campus_management.models import Guest, GlobalNotifications, UserNotifications
from campus_management.choices import GuestStatusChoices, NotificationStatusChoices

class Command(BaseCommand):
    help = 'Esegue tutte le operazioni giornaliere: aggiorna le notti degli ospiti e invia le notifiche programmate.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Inizio esecuzione task giornalieri ---'))

        # --- Logica per aggiornare le notti degli ospiti ---
        self.stdout.write('1. Aggiornamento notti ospiti...')
        in_house_guests = Guest.objects.filter(status=GuestStatusChoices.IN_HOUSE)
        updated_guests_count = 0
        for guest in in_house_guests:
            if guest.checkInTime:
                delta = timezone.now().date() - guest.checkInTime.date()
                guest.nights = delta.days
                guest.save()
                updated_guests_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'-> Aggiornati {updated_guests_count} ospiti.'))

        # --- Logica per inviare notifiche programmate ---
        self.stdout.write('2. Invio notifiche programmate...')
        now = timezone.now()
        
        # Notifiche Globali
        global_notifications_to_send = GlobalNotifications.objects.filter(
            status=NotificationStatusChoices.PROGRAMMATA,
            sendingTime__lte=now 
        )
        global_count = global_notifications_to_send.update(status=NotificationStatusChoices.INVIATA)
        self.stdout.write(self.style.SUCCESS(f'-> Inviate {global_count} notifiche globali.'))

        # Notifiche Utente
        user_notifications_to_send = UserNotifications.objects.filter(
            status=NotificationStatusChoices.PROGRAMMATA,
            sendingTime__lte=now
        )
        user_count = user_notifications_to_send.update(status=NotificationStatusChoices.INVIATA)
        self.stdout.write(self.style.SUCCESS(f'-> Inviate {user_count} notifiche utente.'))

        self.stdout.write(self.style.SUCCESS('--- Task giornalieri completati con successo! ---'))
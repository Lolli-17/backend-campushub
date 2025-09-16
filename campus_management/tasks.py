from celery import shared_task
from django.utils import timezone
from .models import Guest, GlobalNotifications, UserNotifications
from .choices import GuestStatusChoices, NotificationStatusChoices

@shared_task
def update_guest_nights():
	"""
	Questo task controlla tutti gli ospiti che sono attualmente 'IN_HOUSE'
	e calcola il numero di notti trascorse dal loro check-in.
	Viene eseguito ogni giorno a mezzanotte.
	"""
	# Selezioniamo tutti gli ospiti che sono attualmente nello studentato.
	in_house_guests = Guest.objects.filter(status=GuestStatusChoices.IN_HOUSE)
	
	for guest in in_house_guests:
		# Ci assicuriamo che il checkInTime non sia nullo per evitare errori.
		if guest.checkInTime:
			# Calcoliamo la differenza in giorni tra oggi e la data di check-in.
			# Il metodo .date() estrae solo la data (ignorando l'ora).
			delta = timezone.now().date() - guest.checkInTime.date()
			guest.nights = delta.days
			guest.save()
			print(f"Aggiornate le notti per l'ospite {guest.guest_name} a {guest.nights}.")
	
	return f"Aggiornati {in_house_guests.count()} ospiti."


@shared_task
def activate_scheduled_notifications():
	"""
	Questo task controlla le notifiche (sia Globali che Utente) che sono 'PROGRAMMATE'
	e la cui data di invio è passata. Le imposta come 'INVIATE'.
	Viene eseguito ogni minuto.
	"""
	today = timezone.now().date()
	
	# 1. Gestione delle notifiche GLOBALI
	# Selezioniamo le notifiche programmate che devono essere inviate ora.
	global_notifications_to_send = GlobalNotifications.objects.filter(
		status=NotificationStatusChoices.PROGRAMMATA,
		sendingTime__date=today 
	)
	# Aggiorniamo il loro stato a 'INVIATA'
	global_count = global_notifications_to_send.update(status=NotificationStatusChoices.INVIATA)
	
	if global_count > 0:
		print(f"Inviate {global_count} notifiche globali.")
		
	# 2. Gestione delle notifiche UTENTE
	# Facciamo la stessa identica cosa per le notifiche specifiche dell'utente.
	user_notifications_to_send = UserNotifications.objects.filter(
		status=NotificationStatusChoices.PROGRAMMATA,
		sendingTime__date=today
	)
	# Aggiorniamo il loro stato a 'INVIATA'
	user_count = user_notifications_to_send.update(status=NotificationStatusChoices.INVIATA)
	
	if user_count > 0:
		print(f"Inviate {user_count} notifiche utente.")
		
	return f"Task completato. Notifiche globali inviate: {global_count}, Notifiche utente inviate: {user_count}."
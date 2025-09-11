from django.db import models


class ChoiceFieldMixin(models.Model):
	"""
	Mixin generico per modelli che usano un campo con TextChoices.
	"""

	CHOICE_FIELD = 'status'  # override nel modello
	CHOICES_CLASS = None     # override nel modello (es: StatusChoices)

	class Meta:
		abstract = True

	def get_choice_display(self):
		field_value = getattr(self, self.CHOICE_FIELD)
		return self.CHOICES_CLASS(field_value).label if field_value else None

	def set_choice(self, value):
		if value not in self.CHOICES_CLASS.values:
			raise ValueError(f"'{value}' is not a valid choice for {self.CHOICE_FIELD}")
		setattr(self, self.CHOICE_FIELD, value)

	def is_choice(self, value):
		return getattr(self, self.CHOICE_FIELD) == value

	def get_all_choices(self):
		return list(self.CHOICES_CLASS)

	def get_current_choice_label(self):
		return self.get_choice_display()

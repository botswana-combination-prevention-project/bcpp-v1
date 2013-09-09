from django.db import models
from bhp_registration.models import RegisteredSubject


class DeathManager(models.Manager):

    def get_by_natural_key(self, death_date, subject_identifier_as_pk):
        registered_subject = RegisteredSubject.objects.get(subject_identifier_as_pk=subject_identifier_as_pk)
        return self.get(death_date=death_date, registered_subject=registered_subject)

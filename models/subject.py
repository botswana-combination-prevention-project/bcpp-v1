from django.db import models
from bhp_subject.classes import BaseSubject


class Subject (BaseSubject):
       
    subject_consent_id = models.CharField(
        max_length=100, 
        null = True,
        blank = True,
        )
    
    class Meta:
        abstract=True

from django.db import models
from bhp_lab_reference.models import BaseReferenceList

class GradingList(BaseReferenceList):

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = "bhp_lab_grading"
        ordering = ['name']


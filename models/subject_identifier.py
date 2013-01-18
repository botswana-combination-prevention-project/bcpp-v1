from django.db import models
from base_identifier_model import BaseIdentifierModel


class SubjectIdentifier(BaseIdentifierModel):

    objects = models.Manager()

    class Meta:
        app_label = "bhp_identifier"
        ordering = ['-created']

from django.db import models
from bhp_identifier.classes import BaseIdentifierModel


class SubjectIdentifier(BaseIdentifierModel):

    objects = models.Manager()

    class Meta:
        app_label = "bhp_identifier"

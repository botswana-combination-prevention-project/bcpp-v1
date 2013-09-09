from django.db import models
from lab_base_model.models import BaseLabListModel


class BaseAliquotCondition(BaseLabListModel):

    objects = models.Manager()

    def __unicode__(self):
        return "%s: %s" % (self.short_name.upper(), self.name)

    class Meta:
        abstract = True

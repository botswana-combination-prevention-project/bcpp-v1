from django.db import models
from bhp_base_model.classes import BaseListModel


class AliquotCondition(BaseListModel):

    objects = models.Manager()

    def __unicode__(self):
        return "%s: %s" % (self.short_name.upper(), self.name)

    class Meta:
        app_label = 'lab_clinic_api'

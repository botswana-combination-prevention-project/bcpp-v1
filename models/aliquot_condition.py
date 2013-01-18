from django.db import models
from bhp_base_model.models import BaseListModel


class AliquotCondition(BaseListModel):

    objects = models.Manager()

    def __unicode__(self):
        return "%s: %s" % (self.short_name.upper(), self.name)

    class Meta:
        ordering = ["short_name"]
        app_label = 'lab_aliquot_list'
        db_table = 'bhp_lab_core_aliquotcondition'

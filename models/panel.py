from django.db import models
from lab_panel.models import BasePanel


class Panel(BasePanel):

    objects = models.Manager()

    def __unicode__(self):
        return '%s' % (self.name)

    class Meta:
        app_label = 'lab_clinic_api'
        #ordering =['result_identifier']

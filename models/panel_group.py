from django.db import models
from bhp_base_model.models import BaseModel
from lab_clinic_api.managers import PanelGroupManager


class PanelGroup (BaseModel):

    name = models.CharField(
        verbose_name="Panel Group Name",
        max_length=25,
        unique=True,
        )

    objects = PanelGroupManager()

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'lab_panel'
        db_table = 'bhp_lab_core_panelgroup'

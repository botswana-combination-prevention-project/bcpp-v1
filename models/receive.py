from django.db import models
from lab_receive.managers import ReceiveManager
from lab_patient.models import Patient
from bhp_research_protocol.models import Protocol
from bhp_research_protocol.models import Site
from base_receive import BaseReceive


class Receive (BaseReceive):

    protocol = models.ForeignKey(Protocol)

    patient = models.ForeignKey(Patient)

    site = models.ForeignKey(Site)

    dmis_panel_name = models.CharField(
        verbose_name='Panel name on dmis receive record',
        max_length=50,
        null=True)
    dmis_reference = models.IntegerField()

    objects = ReceiveManager()

    def get_absolute_url(self):
        return "/lab_receive/receive/%s/" % self.id

    class Meta:
        app_label = 'lab_receive'
        verbose_name_plural = 'Receive'
        db_table = 'bhp_lab_core_receive'

from django.db import models
from lab_account.models import Account
from lab_test_code.models import TestCode
from lab_aliquot_list.models import AliquotType
from lab_clinic_api.managers import PanelManager
from panel_group import PanelGroup
from base_panel import BasePanel


class Panel(BasePanel):

    panel_group = models.ForeignKey(PanelGroup)

    test_code = models.ManyToManyField(TestCode,
        verbose_name='Test Codes',
        help_text='Choose all that apply',
        )
    aliquot_type = models.ManyToManyField(AliquotType,
        help_text='Choose all that apply',
        )

    account = models.ManyToManyField(Account,
        null=True,
        blank=True
        )

    dmis_panel_identifier = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        )

    objects = PanelManager()

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return (self.name, )
    natural_key.dependencies = ['lab_panel.panel_group']

    class Meta:
        app_label = 'lab_panel'
        db_table = 'bhp_lab_core_panel'
        ordering = ['name', ]

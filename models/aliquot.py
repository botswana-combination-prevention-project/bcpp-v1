from django.db import models
from lab_receive.models import Receive
from lab_aliquot_list.models import AliquotCondition, AliquotType
from lab_aliquot.managers import AliquotManager
from base_aliquot import BaseAliquot


class Aliquot (BaseAliquot):

    receive = models.ForeignKey(Receive)
    aliquot_type = models.ForeignKey(AliquotType,
        verbose_name="Aliquot Type")
    aliquot_condition = models.ForeignKey(AliquotCondition,
        verbose_name="Aliquot Condition",
        default=10,
        null=True)
    parent_identifier = models.ForeignKey('self',
        to_field='aliquot_identifier',
        blank=True,
        null=True)
    subject_identifier = models.CharField(
        max_length=25,
        null=True,
        editable=False,
        db_index=True,
        help_text="non-user helper field to simplify search and filtering")
    objects = AliquotManager()

    def save(self, *args, **kwargs):
        self.subject_identifier = self.receive.patient.subject_identifier
        super(Aliquot, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return "/lab_aliquot/aliquot/%s/" % self.id

    def get_search_url(self):
        return "/laboratory/aliquot/search/aliquot/byword/%s/" % self.id

    class Meta:
        app_label = 'lab_aliquot'
        db_table = 'bhp_lab_core_aliquot'

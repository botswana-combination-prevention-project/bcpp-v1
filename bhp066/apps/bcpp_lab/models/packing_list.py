from django.db import models

from edc.lab.lab_packing.models import BasePackingList

from ..managers import PackingListManager
from .subject_requisition import SubjectRequisition
from .aliquot import Aliquot


class PackingList(BasePackingList):

    community = models.CharField(
        max_length=25,
        null=True,
        blank=False,
    )

    objects = PackingListManager()

    def natural_key(self):
        return (self.timestamp, )

    @property
    def item_models(self):
        return[SubjectRequisition, Aliquot]

    @property
    def packing_list_item_model(self):
        return models.get_model('bcpp_lab', 'PackingListItem')

    class Meta:
        app_label = "bcpp_lab"
        verbose_name = 'Packing List'

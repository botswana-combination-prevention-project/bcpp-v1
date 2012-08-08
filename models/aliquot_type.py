from django.db import models
from base_aliquot_type import BaseAliquotType


class AliquotType(BaseAliquotType):

    dmis_reference = models.IntegerField()

    class Meta:
        ordering = ["name"]
        app_label = 'lab_aliquot_list'
        db_table = 'bhp_lab_core_aliquottype'

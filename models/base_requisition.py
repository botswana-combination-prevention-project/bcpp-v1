from django.db import models
from django.core.serializers.base import SerializationError
from lab_test_code.models import TestCode
from base_base_requisition import BaseBaseRequisition


class BaseRequisition (BaseBaseRequisition):

    # populate this one based on the selected panel at the dashboard
    test_code = models.ManyToManyField(TestCode,
        verbose_name='Additional tests',
        null=True,
        blank=True,
        )

    def natural_key(self):
        raise SerializationError('Requisition subclass must override method \'natural key\'.')

    class Meta:
        abstract = True

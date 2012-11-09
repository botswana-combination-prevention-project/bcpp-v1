from django.db import models
from lab_test_code.models import TestCode
from lab_requisition.classes import BaseBaseRequisition


class BaseRequisition (BaseBaseRequisition):

    # populate this one based on the selected panel at the dashboard
    test_code = models.ManyToManyField(TestCode,
        verbose_name='Additional tests',
        null=True,
        blank=True,
        )

    class Meta:
        abstract = True

from django.db import models
from bhp_common.choices import YES_NO
from bhp_code_lists.models import DxCode
from base_death import BaseDeath


class BaseDeathReport(BaseDeath):

    """
    Death form / AF005
    """
    illness_duration = models.IntegerField(
        verbose_name="4d. Duration of acute illness directly causing death   ",
        help_text="If unknown enter -1",
        )

    perform_autopsy = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="3. Will an autopsy be performed later  ",
        help_text="",
        )

    dx_code = models.ForeignKey(DxCode,
        max_length=25,
        verbose_name="4c. Please code the cause of death as one of the following:",
        help_text="Use diagnosis code from Diagnosis Reference Listing",
        )

    class Meta:
        abstract = True

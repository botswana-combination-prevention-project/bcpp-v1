from django.db import models
from base_code_list import BaseCodeList


class WcsDxAdult(BaseCodeList):

    """WhoClinicalStagingDxAdult"""

    list_ref = models.CharField("List Reference",
        max_length=100,
        blank=True,
        )

    class Meta:
        app_label = "bhp_code_lists"


class WcsDxPed(BaseCodeList):

    """WhoClinicalStagingDxPediatric"""

    list_ref = models.CharField("List Reference",
        max_length=100,
        blank=True,
        )

    class Meta:
        app_label = "bhp_code_lists"


class MedicationCode (BaseCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)

    class Meta:
        app_label = "bhp_code_lists"


class BodySiteCode (BaseCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)

    class Meta:
        app_label = "bhp_code_lists"


class OrganismCode (BaseCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)

    class Meta:
        app_label = "bhp_code_lists"


class ArvCode (BaseCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)

    class Meta:
        app_label = "bhp_code_lists"


class ArvDoseStatus (BaseCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)

    class Meta:
        app_label = "bhp_code_lists"


class ArvModificationCode (BaseCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)

    class Meta:
        app_label = "bhp_code_lists"

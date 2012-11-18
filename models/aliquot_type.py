from lab_aliquot_list.models import BaseAliquotType
from lab_clinic_api.managers import AliquotTypeManager


class AliquotType(BaseAliquotType):

    objects = AliquotTypeManager()

    class Meta:
        ordering = ["name"]
        app_label = 'lab_clinic_api'

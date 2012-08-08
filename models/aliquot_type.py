from lab_aliquot_list.models import BaseAliquotType


class AliquotType(BaseAliquotType):

    class Meta:
        ordering = ["name"]
        app_label = 'lab_clinic_api'

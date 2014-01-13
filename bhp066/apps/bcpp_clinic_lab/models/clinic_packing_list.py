from edc.lab.lab_packing.models import BasePackingList


class ClinicPackingList(BasePackingList):

    class Meta:
        app_label = "bcpp_clinic_lab"
        verbose_name = 'Clinic Packing List'

from lab_packing.models import BasePackingList


class PackingList(BasePackingList):

    class Meta:
        app_label = "bcpp_lab"
        verbose_name = 'Packing List'

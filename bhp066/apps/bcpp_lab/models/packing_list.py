from edc.lab.lab_packing.models import BasePackingList

from ..managers import PackingListManager


class PackingList(BasePackingList):

    objects = PackingListManager()

    def natural_key(self):
        return (self.timestamp, )

    class Meta:
        app_label = "bcpp_lab"
        verbose_name = 'Packing List'

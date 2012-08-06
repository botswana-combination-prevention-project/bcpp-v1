from lab_receive.managers import ReceiveManager
from base_receive import BaseReceive


class Receive (BaseReceive):

    objects = ReceiveManager()

    def get_absolute_url(self):
        return "/lab_receive/receive/%s/" % self.id

    class Meta:
        app_label = 'lab_receive'
        verbose_name_plural = 'Receive'
        db_table = 'bhp_lab_core_receive'


from dmis_receive import DmisReceive


class Dmis(object):

    def __init__(self, debug=False):

        self.debug = debug

    def fetch(self, **kwargs):
        dmis_receive = DmisReceive(debug=self.debug)
        dmis_receive.import_from_dmis()

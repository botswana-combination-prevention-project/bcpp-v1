from bhp_base_admin.admin import BaseModelAdmin
from bhp_crypto import actions


class BaseCryptorModelAdmin (BaseModelAdmin):

    """ Overide ModelAdmin to force username to be saved on add/change and
    other stuff. """

    def __init__(self, *args, **kwargs):
        self.actions.append(actions.encrypt)
        self.actions.append(actions.decrypt)
        super(BaseCryptorModelAdmin, self).__init__(*args, **kwargs)

from bhp_base_model.classes import BaseModelAdmin
from bhp_crypto import actions


class BaseCryptorModelAdmin (BaseModelAdmin):

    """ Overide ModelAdmin to force username to be saved on add/change and
    other stuff. """

    def __init__(self, *args, **kwargs):
        self.actions.append(actions.encrypt)
        self.actions.append(actions.decrypt)
        super(BaseCryptorModelAdmin, self).__init__(*args, **kwargs)

#    def get_readonly_fields(self, request, obj=None):
#
#        super(BaseCryptorModelAdmin, self).get_readonly_fields(request, obj)
#
#        return self.readonly_fields

from django.conf import settings

from edc.core.identifier.classes import BaseIdentifier


class OrderIdentifier(BaseIdentifier):

    def __init__(self):
        identifier_format = '066{community}{sequence}'
        app_name = 'bcpp_lab'
        model_name = 'orderidentifierhistory'
        modulus = 11
        self.community = settings.SITE_CODE
        super(OrderIdentifier, self).__init__(identifier_format=identifier_format,
                                              app_name=app_name, model_name=model_name, modulus=modulus)

    def get_identifier_prep(self, **kwargs):
        """ Users may override to pass non-default keyword arguments to get_identifier
        before the identifier is created."""
        return {'community': self.community}

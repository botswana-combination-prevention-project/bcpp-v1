from bhp_identifier.classes import BaseSubjectIdentifier


class PIdentifier(BaseSubjectIdentifier):

    def __init__(self, identifier_format=None, app_name=None, model_name=None, site_code=None, padding=None, modulus=None, identifier_prefix=None, community=None):
        identifier_format = '{community}{sequence}'
        app_name = 'bcpp_household'
        model_name = 'plotidentifier'
        modulus = 11
        super(PIdentifier, self).__init__(identifier_format, app_name, model_name, site_code, padding, modulus, identifier_prefix, community)

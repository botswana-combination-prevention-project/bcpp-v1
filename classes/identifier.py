from bhp_identifier.classes import BaseSubjectIdentifier


class Identifier(BaseSubjectIdentifier):

    def __init__(self, identifier_format=None, app_name=None, model_name=None, site_code=None, padding=None, modulus=None, identifier_prefix=None):
        identifier_format = '{plot_identifier}{hosehold_number}'
        app_name = 'bcpp_household'
        model_name = 'householdidentifier'
        modulus = 11
        super(Identifier, self).__init__(identifier_format, app_name, model_name, site_code, padding, modulus, identifier_prefix)
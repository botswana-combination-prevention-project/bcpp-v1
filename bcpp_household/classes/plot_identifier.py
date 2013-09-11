from bhp_identifier.classes import BaseIdentifier


class PlotIdentifier(BaseIdentifier):

    def __init__(self, community):
        identifier_format = '{community}{sequence}'
        app_name = 'bcpp_household'
        model_name = 'plotidentifierhistory'
        modulus = 11
        identifier_prefix = ''
        self.set_community(community)
        super(PlotIdentifier, self).__init__(identifier_format, app_name, model_name, modulus, identifier_prefix)

    def set_community(self, value):
        if not value:
            raise TypeError('Attribute \'community\' may not be None for plot identifier')
        self._community = value

    def get_community(self):
        return self._community

    def get_identifier_prep(self, **kwargs):
        """ Users may override to pass non-default keyword arguments to get_identifier
        before the identifier is created."""
        return {'community': self.get_community()}

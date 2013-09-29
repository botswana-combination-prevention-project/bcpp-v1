from edc_core.bhp_identifier.classes import BaseIdentifier


class HouseholdIdentifier(BaseIdentifier):

    def __init__(self, plot_identifier, household_sequence):
        identifier_format = '{plot_identifier}{household_sequence}'
        app_name = 'bcpp_household'
        model_name = 'householdidentifierhistory'
        modulus = 11
        self.set_plot_identifier(plot_identifier)
        self.set_household_sequence(household_sequence)
        is_derived = True
        super(HouseholdIdentifier, self).__init__(identifier_format=identifier_format, app_name=app_name, model_name=model_name, modulus=modulus, is_derived=is_derived)

    def get_identifier_prep(self, **kwargs):
        """ Users may override to pass non-default keyword arguments to get_identifier
        before the identifier is created."""
        return {'plot_identifier': self.get_plot_identifier(), 'household_sequence': self.get_household_sequence()}

    def set_household_sequence(self, value):
        if not value:
            raise TypeError('Attribute \'_household_sequence\' may not be None for household identifier')
        self._household_sequence = value

    def get_household_sequence(self):
        return self._household_sequence

    def set_plot_identifier(self, value):
        """Sets to the plot_identifier less the check digit."""
        if not value:
            raise TypeError('Attribute \'_plot_identifier\' may not be None for household identifier')
        self._plot_identifier = value.split('-')[0]

    def get_plot_identifier(self):
        return self._plot_identifier

from edc.core.identifier.classes import BaseIdentifier


class HouseholdIdentifier(BaseIdentifier):

    def __init__(self, plot_identifier):
        identifier_format = '{plot_identifier}{household_sequence}'
        app_name = 'bcpp_household'
        model_name = 'householdidentifierhistory'
        modulus = 11
        is_derived = True
        super(HouseholdIdentifier, self).__init__(identifier_format=identifier_format, app_name=app_name, model_name=model_name, modulus=modulus, is_derived=is_derived)
        self.set_plot_identifier(plot_identifier)
        self.set_household_sequence()

    def get_identifier_history_model_options(self):
        """Users may override to add additional options."""
        return {'household_sequence': self.get_household_sequence(), 'plot_identifier': self.get_plot_identifier()}

    def get_identifier_prep(self, **kwargs):
        """ Users may override to pass non-default keyword arguments to get_identifier
        before the identifier is created."""
        return {'plot_identifier': self.get_plot_identifier(), 'household_sequence': self.get_household_sequence()}

    def set_household_sequence(self):
        self._household_sequence = 1
        # check if sequence has been used
        identifier_history_instances = self.get_identifier_history_model().objects.filter(plot_identifier=self.get_plot_identifier())
        sequences_in_use = [identifier_history_instance.identifier.split(self.get_plot_identifier())[1].split('-')[0] for identifier_history_instance in identifier_history_instances]
        if unicode(self._household_sequence) in sequences_in_use:
            self._household_sequence = 1
            while unicode(self._household_sequence) in sequences_in_use:
                self._household_sequence += 1

    def get_household_sequence(self):
        return self._household_sequence

    def set_plot_identifier(self, value):
        """Sets to the plot_identifier less the check digit."""
        if not value:
            raise TypeError('Attribute \'_plot_identifier\' may not be None for household identifier')
        self._plot_identifier = value.split('-')[0]

    def get_plot_identifier(self):
        return self._plot_identifier

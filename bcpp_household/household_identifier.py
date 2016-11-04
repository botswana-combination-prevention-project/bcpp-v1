from edc_identifier.alphanumeric_identifier import AlphanumericIdentifier


class HouseholdIdentifier(AlphanumericIdentifier):

    def __init__(self, plot_identifier):
        identifier_format = '{plot_identifier}{household_sequence}'
        app_name = 'bcpp_household'
        model_name = 'householdidentifierhistory'
        modulus = 11
        is_derived = True
        super(HouseholdIdentifier, self).__init__(
            identifier_format=identifier_format,
            app_name=app_name,
            model_name=model_name,
            modulus=modulus,
            is_derived=is_derived)
        self.plot_identifier = plot_identifier

    def __repr__(self):
        return 'HouseholdIdentifier({0.plot_identifier!r})'.format(self)

    def __str__(self):
        return '({0.plot_identifier!r}})'.format(self)

    def get_identifier_history_model_options(self):
        return {'household_sequence': self.household_sequence, 'plot_identifier': self.plot_identifier}

    def get_identifier_prep(self, **kwargs):
        return {'plot_identifier': self.plot_identifier, 'household_sequence': self.household_sequence}

    @property
    def household_sequence(self):
        self._household_sequence = 1
        identifier_history_instances = self.get_identifier_history_model().objects.filter(
            plot_identifier=self.plot_identifier)
        sequences_in_use = [
            identifier_history_instance.identifier.split(self.plot_identifier)[1].split('-')[0]
            for identifier_history_instance in identifier_history_instances]
        if str(self._household_sequence) in sequences_in_use:
            self._household_sequence = 1
            while str(self._household_sequence) in sequences_in_use:
                self._household_sequence += 1
        return self._household_sequence

    @property
    def plot_identifier(self):
        return self._plot_identifier

    @plot_identifier.setter
    def plot_identifier(self, value):
        """Sets to the plot_identifier less the check digit."""
        if not value:
            raise TypeError('Attribute \'_plot_identifier\' may not be None for household identifier')
        self._plot_identifier = value.split('-')[0]

from django.db import models


class ConfigurationManager(models.Manager):

    def get_by_natural_key(self, allowed_iso_weekdays):
        return self.get(allowed_iso_weekdays=allowed_iso_weekdays)

    def get_configuration(self):

        """ Returns only the first record """

        configuration = super(ConfigurationManager, self).all().order_by('created')
        if not configuration:
            raise ValueError('Appointment.configuration model has no entry. Please fill in values for this model')
        else:
            configuration = configuration[0]
        return configuration

from django.db import models

class ConfigurationManager(models.Manager):

    def get_configuration(self):

        """ return only the first record """

        configuration = super(ConfigurationManager, self).all().order_by('created')
        if not configuration:
            raise ValueError, 'Appointment.configuration model has no entry. Please fill in values for this model'
        else:
            configuration = configuration[0]
        return configuration            


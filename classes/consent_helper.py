from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db import models
from bhp_consent.models import BaseConsent, ConsentCatalogue


class ConsentHelper(object):

    def get_current_consent_version(self, consent, instance_datetime):
        """Returns the current consent version relative to the given instance_datetime.
        
        Arguments:
            consent: either the name of the consent as defined in ConsentCatalogue or an instance of the consent"""
        current_consent_version = None
        #ConsentCatalogue = models.get_model('bhp_consent', 'ConsentCatalogue')
        if isinstance(consent, BaseConsent):
            consent_catalogues = ConsentCatalogue.objects.filter(consent_instance=consent)
            #raise TypeError('Argument \'consent_instance\' must be an instance of BaseConsent.')
        elif isinstance(consent, basestring):
            consent_catalogues = ConsentCatalogue.objects.filter(name=consent)
        for consent_catalogue in consent_catalogues:
            end_date = consent_catalogue.end_datetime or datetime.today() + relativedelta(days=1)
            if instance_datetime >= consent_catalogue.start_datetime and instance_datetime < end_date:
                current_consent_version = consent_catalogue.version
        if not current_consent_version:
            raise TypeError('Cannot determine the version of consent \'{0}\' using \'{1}\''.format(consent, instance_datetime))
        return current_consent_version

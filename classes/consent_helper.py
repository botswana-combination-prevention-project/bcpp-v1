from datetime import datetime
from dateutil.relativedelta import relativedelta
from bhp_consent.models import ConsentCatalogue, AttachedModel


class ConsentHelper(object):

    def __init__(self, subject_instance):
        self._report_datetime = None
        self._subject_identifier = None
        self._current_consent_version = None
        self._consent_models = []
        self._subject_instance = subject_instance

    def get_subject_instance(self):
        return self._subject_instance

    def get_current_consent_version(self):
        """Returns the current consent version relative to the given subject_instance report_datetime and subject_identifier."""
        for consent_catalogue in ConsentCatalogue.objects.filter(content_type_map__model__in=[consent_model._meta.object_name.lower() for consent_model in self.get_consent_models()]):
            end_date = consent_catalogue.end_datetime or datetime.today() + relativedelta(days=1)
            if self.get_report_datetime() >= consent_catalogue.start_datetime and self.get_report_datetime() < end_date:
                current_consent_version = consent_catalogue.version
        if not current_consent_version:
            raise TypeError('Cannot determine the version of consent \'{0}\' using \'{1}\''.format(self.get_subject_instance(), self.get_report_datetime()))
        return current_consent_version

    def set_report_datetime(self):
        """Sets the datetime field to use to compare with the consent start and end dates."""
        self._report_datetime = None
        if 'get_report_datetime' in dir(self.get_subject_instance()):
            self._report_datetime = self.get_subject_instance().get_report_datetime()
        elif 'get_visit' in dir(self.get_subject_instance()):
            self._report_datetime = self.get_subject_instance().get_visit().report_datetime
        elif 'report_datetime' in dir(self.get_subject_instance()):
            self._report_datetime = self.get_subject_instance().report_datetime
        elif 'registration_datetime' in dir(self.get_subject_instance()):
            self._report_datetime = self.get_subject_instance().registration_datetime
        else:
            raise TypeError('Cannot determine datetime to use for model {0} to compare with the consent catalogue. Add get_report_datetime() to the model.'.format(self.get_subject_instance()._meta.object_name))

    def get_report_datetime(self):
        if not self._report_datetime:
            self.set_report_datetime()
        return self._report_datetime

    def set_subject_identifier(self):
        """Gets the subject_identifier from the instance."""
        self._subject_identifier = None
        if 'subject_identifier' in dir(self.get_subject_instance()):
            self._subject_identifier = self.get_subject_instance().subject_identifier
        elif 'get_subject_identifier' in dir(self.get_subject_instance()):
            self._subject_identifier = self.get_subject_instance().get_subject_identifier()
        elif 'get_visit' in dir(self.get_subject_instance()):
            self._subject_identifier = self.get_subject_instance().get_visit().get_subject_identifier()
        else:
            raise TypeError('Cannot determine the subject_identifier for model {0} needed to lookup the consent. Perhaps add method get_subject_identifier() to the model.'.format(self.get_subject_instance()._meta.object_name))

    def get_subject_identifier(self):
        if not self._subject_identifier:
            self.set_subject_identifier()
        return self._subject_identifier

    def set_consent_models(self):
        """Sets consent models for this instance by querying the AttachedModel class."""
        self._consent_models = []
        # find if any consent models listed in the catalogue cover this report_datetime
        for attached_model in AttachedModel.objects.filter(content_type_map__model=self._meta.object_name.lower()):
            if self.get_report_datetime() >= attached_model.consent_catalogue.start_datetime and self.get_report_datetime() < attached_model.consent_catalogue.end_datetime:
                self._consent_models.append(attached_model.consent_catalogue.content_type_map.content_type.model_class())
        if not self._consent_models:
            raise TypeError('Cannot determine the consent model class for this model instance {0}'.format(self.get_subject_instance()._meta.object_name))

    def get_consent_models(self):
        """Gets consent models for this subject_instance."""
        if not self._consent_models:
            self.set_consent_models()
        return self._consent_models

    def is_consented_for_subject_instance(self):
        retval = False
        for consent_model in self.get_consent_models():
            if consent_model.objects.filter(subject_identifier=self.get_subject_identifier()).exists():
                # confirm what version covers either from consent model or consent_update_model_cls
                # does the catalogue return only the MaternalConsent, ??
                retval = True
                # look for an updated consent attached to this model
                # TODO: look up in consent_update_model_cls ??
                #retval = True
        return retval

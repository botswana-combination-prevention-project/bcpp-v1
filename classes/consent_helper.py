from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.db.models import get_model


class ConsentHelper(object):

    def __init__(self, subject_instance, exception_cls=None):
        self._report_datetime = None
        self._subject_identifier = None
        self._current_consent_version = None
        self._consent_models = []
        self._subject_instance = subject_instance
        self.set_exception_cls(exception_cls)

    def set_exception_cls(self, cls=None):
        if cls:
            self._exception_cls = cls
        else:
            self._exception_cls = ValidationError

    def get_exception_cls(self):
        return self._exception_cls

    def get_subject_instance(self):
        return self._subject_instance

    def get_current_consent_version(self):
        """Returns the current consent version relative to the given subject_instance report_datetime and subject_identifier."""
        ConsentCatalogue = get_model('bhp_consent', 'ConsentCatalogue')
        for consent_catalogue in ConsentCatalogue.objects.filter(content_type_map__model__in=[consent_model._meta.object_name.lower() for consent_model in self.get_consent_models()]):
            end_date = consent_catalogue.end_datetime or datetime.today() + relativedelta(days=1)
            if self.get_report_datetime() >= consent_catalogue.start_datetime and self.get_report_datetime() < end_date:
                current_consent_version = consent_catalogue.version
        if not current_consent_version:
            raise self.get_exception_cls()('Cannot determine the version of consent \'{0}\' using \'{1}\''.format(self.get_subject_instance(), self.get_report_datetime()))
        return current_consent_version

    def set_report_datetime(self):
        """Sets the datetime field to use to compare with the consent start and end dates.

        The report_datetime comes from the subject_instance"""

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
            raise self.get_exception_cls()('Cannot determine datetime to use for model {0} to compare with the consent catalogue. Add get_report_datetime() to the model.'.format(self.get_subject_instance()._meta.object_name))

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
            raise self.get_exception_cls()('Cannot determine the subject_identifier for model {0} needed to lookup the consent. Perhaps add method get_subject_identifier() to the model.'.format(self.get_subject_instance()._meta.object_name))

    def get_subject_identifier(self):
        if not self._subject_identifier:
            self.set_subject_identifier()
        return self._subject_identifier

    def set_consent_models(self):
        """Sets consent models for this instance by querying the AttachedModel class."""
        self._consent_models = []
        AttachedModel = get_model('bhp_consent', 'AttachedModel')
        # find if any consent models listed in the catalogue cover this report_datetime
        for attached_model in AttachedModel.objects.filter(content_type_map__model=self.get_subject_instance()._meta.object_name.lower()):
            if self.get_report_datetime() >= attached_model.consent_catalogue.start_datetime and self.get_report_datetime() < attached_model.consent_catalogue.end_datetime:
                self._consent_models.append(attached_model.consent_catalogue.content_type_map.content_type.model_class())
        if not self._consent_models:
            raise self.get_exception_cls()('Cannot determine the consent model class for this model instance {0}'.format(self.get_subject_instance()._meta.object_name))

    def get_consent_models(self):
        """Gets consent models for this subject_instance."""
        if not self._consent_models:
            self.set_consent_models()
        return self._consent_models

    def is_consented_for_subject_instance(self):
        consent_models = []
        for consent_model in self.get_consent_models():
            if consent_model.objects.filter(subject_identifier=self.get_subject_identifier()):
                # confirm what version covers either from consent model or consent_update_model_cls
                # does the catalogue return only the MaternalConsent, ??
                consent_models.append(consent_model.objects.get(subject_identifier=self.get_subject_identifier()))
                # look for an updated consent attached to this model
                # TODO: look up in consent_update_model_cls ??
                #retval = True
        return consent_models

    def validate_versioned_fields(self):
        """Validate fields under consent version control to be set to the default value or not (None).

        This validation logic should also be applied in the forms.py along with more field
        specific validation logic."""
        ConsentCatalogue = get_model('bhp_consent', 'ConsentCatalogue')
        current_consent_version = self.get_current_consent_version()
        # cycle through all versions in the consent catalogue
        for consent_catalogue in ConsentCatalogue.objects.all().order_by('start_datetime', 'version'):
            consent_version = consent_catalogue.version
            start_datetime = consent_catalogue.start_datetime
            if not start_datetime:
                raise TypeError('Cannot determine consent version start date. Check the Consent Catalogue')
            if self.get_subject_instance().get_versioned_field_names(consent_version):
                for field in self.get_subject_instance()._meta.fields:
                    if field.name in self.get_subject_instance().get_versioned_field_names(consent_version):
                        field_value = getattr(self.get_subject_instance(), field.name)
                        if self.get_report_datetime() < start_datetime and field_value:
                            # enforce None / default
                            raise self.get_exception_cls()('Field \'{0}\' must be left blank for data captured prior to version {2}.'.format(field.name, start_datetime, consent_version))
                        if self.get_report_datetime() >= start_datetime and not field_value:
                            # require a user provided value
                            raise self.get_exception_cls()('Field \'{0}\' cannot be blank for data captured during or after version {2}.'.format(field.name, start_datetime, consent_version))
        return current_consent_version

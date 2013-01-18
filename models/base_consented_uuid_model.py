from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db import models
from bhp_sync.classes import BaseSyncUuidModel


class BaseConsentedUuidModel(BaseSyncUuidModel):

    """Base model class for all models that collect data requiring consent. """

    def is_consented_for_model(self):
        """Confirms subject has a consent that covers data entry for this model."""
        report_datetime = None
        subject_identifier = None
        consent_models = []
        retval = False
        # guess which field to use to compare with the consent start and end dates
        if 'get_report_datetime' in dir(self):
            report_datetime = self.get_report_datetime()
        elif 'get_visit' in dir(self):
            report_datetime = self.get_visit().report_datetime
        elif 'report_datetime' in dir(self):
            report_datetime = self.report_datetime
        elif 'registration_datetime' in dir(self):
            report_datetime = self.registration_datetime
        else:
            raise TypeError('Cannot determine datetime to use for model {0} to compare with the consent catalogue. Add get_report_datetime() to the model.'.format(self._meta.object_name))

        # guess how to get the subject_identifier
        if 'subject_identifier' in dir(self):
            subject_identifier = self.subject_identifier
        elif 'get_subject_identifier' in dir(self):
            subject_identifier = self.get_subject_identifier()
        elif 'get_visit' in dir(self):
            subject_identifier = self.get_visit().get_subject_identifier()
        else:
            raise TypeError('Cannot determine the subject_identifier for model {0} needed to lookup the consent. Perhaps add method get_subject_identifier() to the model.'.format(self._meta.object_name))
        # get the instances of consent_catalogue for this model using the AttahcedModel class.
        AttachedModel = models.get_model('bhp_consent', 'attachedmodel')
        # find if any consent models listed in the catalogue cover this report_datetime
        for consent_catalogue in [attached_model.consent_catalogue for attached_model in AttachedModel.objects.filter(content_type_map__model=self._meta.object_name.lower())]:
            if report_datetime >= attached_model.consent_catalogue.start_datetime and report_datetime < attached_model.consent_catalogue.end_datetime:
                consent_models.append(consent_catalogue.content_type_map.content_type.model_class())
        if not consent_models:
            raise TypeError('Cannot determine the consent for this model {0}'.format(self._meta.object_name))
        # query the consent models for this subject
        if consent_models:
            for consent_model in consent_models:
                if consent_model.objects.filter(subject_identifier=subject_identifier).exists():
                    # confirm what version covers either from consent model or consent_update_model_cls
                    # does the catalogue return only the MaternalConsent, ??
                    retval = True
                    # look for an updated consent attached to this model
                    consent_update_model_cls = consent_model.get_consent_update_model()
                    # TODO: look up in consent_update_model_cls
                    #retval = True
        return retval

    def get_current_consent_version(self, name, instance_datetime):
        """Returns the current consent version relative to the given instance_datetime."""
        current_consent_version = None
        ConsentCatalogue = models.get_model('bhp_consent', 'ConsentCatalogue')
        for consent_catalogue in ConsentCatalogue.objects.filter(name=name):
            end_date = consent_catalogue.end_datetime or datetime.today() + relativedelta(days=1)
            if instance_datetime >= consent_catalogue.start_datetime and instance_datetime < end_date:
                current_consent_version = consent_catalogue.version
        if not current_consent_version:
            raise TypeError('Cannot determine the version of consent \'{0}\' using \'{1}\''.format(name, instance_datetime))
        return current_consent_version

    def get_versioned_field_names(self, version_number):
        """Returns a list of field names under version control by version number.

        Users should override at the model class to return a list of field names for a given version_number."""
        return []

    def validate_versioned_fields(self, consent_instance, instance_datetime, cleaned_data=None, exception_cls=None):
        """Validate fields under consent version control to be set to the default value or not (None).

        This validation logic should also be applied in the forms.py along with more field
        specific validation logic."""
        ConsentCatalogue = models.get_model('bhp_consent', 'ConsentCatalogue')
        consent_name = self.get_consent_name()
        current_consent_version = self.get_current_consent_version(consent_name, instance_datetime)
        if not cleaned_data:
            cleaned_data = {}
        if not exception_cls:
            exception_cls = ValueError
        # cycle through all versions in the consent catalogue
        for consent_catalogue in ConsentCatalogue.objects.all().order_by('start_datetime', 'version'):
            consent_version = consent_catalogue.version
            start_datetime = consent_catalogue.start_datetime
            if not start_datetime:
                raise TypeError('Cannot determine consent version start date. Check settings.py attribute CONSENT_VERSIONS')
            if self.get_versioned_field_names(consent_version):
                for field in self._meta.fields:
                    if field.name in self.get_versioned_fields_list(consent_version):
                        field_value = getattr(self, field.name) or cleaned_data.get(field.name, None)
                        if instance_datetime < start_datetime and field_value:
                            # enforce None / default
                            raise exception_cls('Field \'{0}\' must be left blank for data captured prior to version {2}.'.format(field.name, start_datetime, consent_version))
                        if instance_datetime >= start_datetime and not field_value:
                            # require a user provided value
                            raise exception_cls('Field \'{0}\' cannot be blank for data captured during or after version {2}.'.format(field.name, start_datetime, consent_version))
        return current_consent_version

    def save(self, *args, **kwargs):
        if not self.is_consented_for_model():
            raise TypeError('Entry not permitted. Model {0} is not covered by a valid consent for this subject.'.format(self._meta.object_name))
        super(BaseConsentedUuidModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True

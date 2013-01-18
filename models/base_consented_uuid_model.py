from django.db import models
from bhp_sync.classes import BaseSyncUuidModel
from bhp_consent.classes import ConsentHelper


class BaseConsentedUuidModel(BaseSyncUuidModel, ConsentHelper):

    """Base model class for all models that collect data requiring consent. """

    def is_consented_for_model(self):
        """Confirms subject has a consent that covers data entry for this model."""
        return consent_helper.is_consented_for_instance(self)

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
        current_consent_version = self.get_current_consent_version(consent_instance, instance_datetime)
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

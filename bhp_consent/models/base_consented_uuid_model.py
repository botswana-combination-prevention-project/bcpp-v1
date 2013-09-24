from django.conf import settings
if 'bhp_dispatch' in settings.INSTALLED_APPS:
    from bhp_dispatch.models import BaseDispatchSyncUuidModel as BaseSyncUuidModel
else:
    from bhp_sync.models import BaseSyncUuidModel
from bhp_off_study.exceptions import SubjectOffStudyError
from bhp_consent.classes import ConsentHelper


class BaseConsentedUuidModel(BaseSyncUuidModel):

    """Base model class for all models that collect data requiring consent. """

    def is_consented_for_instance(self):
        """Confirms subject has a consent that covers data entry for this model."""
        return self.get_consent_helper_cls()(self).is_consented_for_subject_instance()

    def get_versioned_field_names(self, version_number):
        """Returns a list of field names under version control by version number.

        Users should override at the model class to return a list of field names for a given version_number."""
        return []

    def get_consent_helper_cls(self):
        """Returns an instance of the default ConsentHelper."""
        return ConsentHelper

    def validate_versioned_fields(self, cleaned_data=None, exception_cls=None, **kwargs):
        """Validate fields under consent version control to be set to the default value or not (None)."""
        return self.get_consent_helper_cls()(self).validate_versioned_fields()

    def get_requires_consent(self):
        """Users may override to return False to bypass consent checks for this model instance."""
        return True

    def save(self, *args, **kwargs):
        if 'is_off_study' in dir(self):
            if self.is_off_study():
                raise SubjectOffStudyError('Model cannot be saved. Subject is off study. Perhaps catch this exception in forms clean() method.')
        super(BaseConsentedUuidModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True

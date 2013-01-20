from django import forms
#from django.db.models import get_model
from bhp_consent.classes import ConsentHelper
from bhp_base_form.classes import BaseModelForm
from bhp_consent.models import AttachedModel


class BaseConsentedModelForm(BaseModelForm):

    """Base Form for all models that confirm a valid subject consent to be available before allowing data collection."""

    def __init__(self, *args, **kwargs):
        self.check_attached()
        super(BaseModelForm, self).__init__(*args, **kwargs)

    def check_attached(self):
        """Confirms only that model exists in AttachedModel of the Consent Catalogue.

        This does not filter by consent_version, because we don't know it here, which means you may not get the result you expect.
        For example, if a model is to be added/changed under version 1 but is listed for both version 1
        and version 2 where v1 is inactive and v2 is active, an error will NOT be raised here since the query will True for the version 2 model."""
        # AttachedModel = get_model('bhp_consent', 'AttachedModel')
        if not AttachedModel.objects.filter(content_type_map__model=self._meta.model._meta.object_name.lower(), is_active=True).exists():
            raise AttributeError('Models registered to BaseConsentModelForm must be listed, and active, '
                                 'in AttachedModel of the ConsentCatalogue. Model {0} not found or not active.'.format(self._meta.model._meta.object_name.lower()))

    def clean(self):
        """Checks if subject has a valid consent for this subject model instance."""
        cleaned_data = self.cleaned_data
        #check if consented to complete this form
        #check to remove m2m fields from cleaned data
        field_names = [field.name for field in self._meta.model._meta.fields]
        del_keys = [k for k in cleaned_data.iterkeys() if k not in field_names]
        for k in del_keys:
            del cleaned_data[k]
        ConsentHelper(self._meta.model(**cleaned_data), forms.ValidationError).is_consented_for_subject_instance()

        return super(BaseConsentedModelForm, self).clean()

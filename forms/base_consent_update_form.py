from django import forms


class BaseConsentUpdateForm (forms.ModelForm):

    def clean(self, consent_instance_field_name, consent_instance=None):
        cleaned_data = self.cleaned_data
        consent_version = cleaned_data.get('consent_version', None)
        consent_datetime = cleaned_data.get('consent_datetime', None)
        consent_catalogue = cleaned_data.get('consent_catalogue', None)
        if not consent_version and consent_instance:
            # get the consent version and check if duplicate
            consent_version = self._meta.model().get_current_consent_version(consent_catalogue.name, consent_datetime)
            options = {consent_instance_field_name: consent_instance, 'consent_version': consent_version}
            if consent_version == 1:
                raise forms.ValidationError('Consent update cannot have a consent datetime within the consent period for version 1.')
            if self._meta.model.objects.filter(**options).exists() and not cleaned_data.get('id', None):
                raise forms.ValidationError('Consent update for consent version {0} already exists.'.format(consent_version))

        return cleaned_data

from django import forms
from bhp_consent.forms import BaseConsentedModelForm


class BaseOffStudyForm(BaseConsentedModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        self._meta.model().check_off_study_date(cleaned_data.get('registered_subject').get_subject_identifier(), cleaned_data.get('offstudy_date'), exception_cls=forms.ValidationError)
        return super(BaseOffStudyForm, self).clean()

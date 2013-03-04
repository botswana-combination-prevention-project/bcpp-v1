from django import forms
from bhp_consent.models import TestSubjectUuidModel
from bhp_consent.forms import BaseConsentedModelForm


class TestSubjectUuidModelForm (BaseConsentedModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return super(TestSubjectUuidModelForm, self).clean()

    class Meta:
        model = TestSubjectUuidModel

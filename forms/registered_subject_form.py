from django import forms
from bhp_registration.models import RegisteredSubject


class RegisteredSubjectForm (forms.ModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = RegisteredSubject

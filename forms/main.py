from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import SubjectLocator, SubjectDeath, RecentPartner, SecondPartner, ThirdPartner


# SubjectLocator
class SubjectLocatorForm (BaseSubjectModelForm):

    class Meta:
        model = SubjectLocator


# SubjectDeath
class SubjectDeathForm (BaseSubjectModelForm):

    class Meta:
        model = SubjectDeath


#RecentPartner
class RecentPartnerForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = RecentPartner


# SecondPartner
class SecondPartnerForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = SecondPartner


# ThirdPartner
class ThirdPartnerForm (BaseSubjectModelForm):
    def clean(self):

        cleaned_data = self.cleaned_data

        return cleaned_data

    class Meta:
        model = ThirdPartner

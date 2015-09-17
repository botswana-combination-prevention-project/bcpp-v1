from django import forms

#from edc.subject.consent.forms import BaseConsentedModelForm

from ..models import SubjectVisit


class SubjectVisitForm (forms.ModelForm):

    class Meta:
        model = SubjectVisit

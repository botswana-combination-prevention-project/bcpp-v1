from django import forms
from bhp_consent.forms import BaseSubjectConsentForm
from bcpp_subject.models import SubjectConsent


# SubjectConsent
class SubjectConsentForm (BaseSubjectConsentForm):

    class Meta:
        model = SubjectConsent

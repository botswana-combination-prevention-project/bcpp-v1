from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import SubjectLocator


# SubjectLocator
class SubjectLocatorForm (BaseSubjectModelForm):

    class Meta:
        model = SubjectLocator

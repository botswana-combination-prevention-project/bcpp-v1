from django import forms
from base_subject_model_form import BaseSubjectModelForm
from bcpp_subject.models import HivResult


class HivResultForm (BaseSubjectModelForm):

    class Meta:
        model = HivResult

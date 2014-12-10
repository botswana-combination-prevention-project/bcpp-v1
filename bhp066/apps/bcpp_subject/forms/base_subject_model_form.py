from django import forms
from django.conf import settings

from edc.subject.consent.forms import BaseConsentedModelForm

from apps.bcpp_survey.models import Survey

from ..models import SubjectVisit


class BaseSubjectModelForm(BaseConsentedModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseSubjectModelForm, self).__init__(*args, **kwargs)
        try:
            self.fields['subject_visit'].queryset = SubjectVisit.objects.filter(pk=self.instance.subject_visit.pk)
        except:
            pass

    def clean(self):
        cleaned_data = super(BaseSubjectModelForm, self).clean()
        try:
            if settings.LIMIT_EDIT_TO_CURRENT_SURVEY:
                current_survey = Survey.objects.current_survey()
                if cleaned_data.get('subject_visit').household_member.household_structure.survey != current_survey:
                    raise forms.ValidationError('Form may not be saved. Only data from {} may be added/changed. (LIMIT_EDIT_TO_CURRENT_SURVEY)'.format(current_survey))
        except AttributeError:
            pass
        return cleaned_data

from django import forms
from django.conf import settings

from edc.map.classes import site_mappers

from bhp066.apps.bcpp_survey.models import Survey

from ..models import SubjectVisit

from .base_model_form import BaseModelForm


class BaseSubjectModelForm(BaseModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseSubjectModelForm, self).__init__(*args, **kwargs)
        try:
            self.fields['subject_visit'].queryset = SubjectVisit.objects.filter(pk=self.instance.subject_visit.pk)
        except:
            pass

    def clean(self):
        cleaned_data = super(BaseSubjectModelForm, self).clean()
        self.limit_edit_to_current_community(cleaned_data)
        self.limit_edit_to_current_survey(cleaned_data)
        return cleaned_data

    def limit_edit_to_current_survey(self, cleaned_data):
        """Raises an exception if the instance does not refer to the
        current survey OR does nothing,"""
        try:
            if settings.LIMIT_EDIT_TO_CURRENT_SURVEY:
                current_survey = Survey.objects.current_survey()
                survey = cleaned_data.get('subject_visit').household_member.household_structure.survey
                if survey != current_survey:
                    raise forms.ValidationError(
                        'Form may not be saved. Only data from {} may be added/changed. '
                        '(LIMIT_EDIT_TO_CURRENT_SURVEY)'.format(current_survey))
        except AttributeError:
            pass
        return cleaned_data

    def limit_edit_to_current_community(self, cleaned_data):
        """Raises an exception if the instance does not refer to the
        current community OR does nothing,"""
        try:
            if settings.LIMIT_EDIT_TO_CURRENT_COMMUNITY:
                configured_community = site_mappers.get_current_mapper().map_area
                community = cleaned_data.get(
                    'subject_visit').household_member.household_structure.household.plot.community
                if community != configured_community:
                    raise forms.ValidationError(
                        'Form may not be saved. Only data from \'{}\' may be added/changed on '
                        'this device. Got {}. (LIMIT_EDIT_TO_CURRENT_COMMUNITY)'.format(
                            configured_community, community))
        except AttributeError:
            pass
        return cleaned_data

from django.contrib import admin

from edc.subject.visit_tracking.admin import BaseVisitTrackingModelAdmin

from apps.bcpp_survey.models import Survey

from ..models import SubjectVisit, SubjectConsent
from ..constants import BASELINE


class SubjectVisitModelAdmin (BaseVisitTrackingModelAdmin):

    """Model Admin for models with a foreignkey to the subject visit model."""

#     def __init__(self, *args, **kwargs):
#         super(SubjectVisitModelAdmin, self).__init__(*args, **kwargs)

    visit_model = SubjectVisit
    visit_model_foreign_key = 'subject_visit'
    dashboard_type = 'subject'
    date_heirarchy = 'subject_visit__report_datetime'
    current_survey = Survey.objects.current_survey().survey_slug
    first_survey = Survey.objects.first_survey.survey_slug
    baseline_fields = None
    annual_fields = None
    baseline_radio_fields = None
    annual_radio_fields = None
    baseline_instructions = None
    annual_instructions = None

    def get_fieldsets(self, request, obj=None):
        """Returns fieldsets based on the survey, baseline or annual."""
        fieldsets = super(SubjectVisitModelAdmin, self).get_fieldsets(request, obj)
#         subject_consent = None
#         fieldsets[0][1]['fields'] = self.baseline_fields or self.fields
#         try:
#             survey_slug = obj.subject_visit.household_member.household_structure.survey.survey_slug
#         except (AttributeError, ):
#             try:
#                 subject_consent = SubjectConsent.objects.get(registered_subject=request.GET.get('registered_subject'))
#                 survey_slug = subject_consent.household_member.survey.survey_slug
#             except (AttributeError, SubjectConsent.DoesNotExist):
#                 survey_slug = None
#         if survey_slug != self.current_survey:
#             try:
#                 fieldsets[0][1]['fields'] = self.annual_fields or self.fields
#             except AttributeError:
#                 pass
        return fieldsets

    def formfield_for_choice_field(self, db_field, request=None, **kwargs):
        """
        Returns a form Field based on the survey, baseline or annual, for a database
        Field that has declared choices.
        """
        if self.fields == self.annual_fields:
            self.radio_fields = self.annual_radio_fields or self.radio_fields
        else:
            self.radio_fields = self.baseline_radio_fields or self.radio_fields
        return super(SubjectVisitModelAdmin, self).formfield_for_choice_field(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
        Get a form Field for a ForeignKey based on the survey, baseline or annual.
        """
        if self.fields == self.annual_fields:
            self.radio_fields = self.annual_radio_fields or self.radio_fields
        else:
            self.radio_fields = self.baseline_radio_fields or self.radio_fields
        return super(SubjectVisitModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def add_view(self, request, form_url='', extra_context=None):
        """Set the instructions based on the survey, baseline or annual."""
        subject_visit = SubjectVisit.objects.get(pk=request.GET.get('subject_visit'))
        if subject_visit.appointment.visit_definition.code == BASELINE:
            self.fields = self.baseline_fields
            self.instructions = self.baseline_instructions or self.instructions
        else:
            self.fields = self.annual_fields
            self.instructions = self.annual_instructions or self.instructions
        return super(SubjectVisitModelAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Set the instructions based on the survey, baseline or annual."""
        subject_visit = SubjectVisit.objects.get(pk=request.GET.get('subject_visit'))
        if subject_visit.appointment.visit_definition.code == BASELINE:
            self.fields = self.baseline_fields
            self.instructions = self.baseline_instructions or self.instructions
        else:
            self.fields = self.annual_fields
            self.instructions = self.annual_instructions or self.instructions
        return super(SubjectVisitModelAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)

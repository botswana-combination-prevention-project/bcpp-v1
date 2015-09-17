from edc.subject.visit_tracking.admin import BaseVisitTrackingModelAdmin

from bhp066.apps.bcpp_survey.models import Survey

from ..constants import ANNUAL, ANNUAL_CODES
from ..models import SubjectVisit


class SubjectVisitModelAdmin (BaseVisitTrackingModelAdmin):

    """Model Admin for models with a foreignkey to the subject visit model."""

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

    def __init__(self, *args, **kwargs):
        self.subject_visit = None
        super(BaseVisitTrackingModelAdmin, self).__init__(*args, **kwargs)
        if not self.date_hierarchy:
            self.date_hierarchy = 'created'
        self.list_filter = list(self.list_filter)
        try:
            self.list_filter.remove('subject_visit')
        except ValueError:
            pass
        self.list_filter.extend(['created', 'modified', 'hostname_created', 'hostname_modified'])
        self.list_filter = list(set(self.list_filter))
        self.search_fields = list(self.search_fields)
        try:
            self.search_fields.index('subject_visit__appointment__registered_subject__identity')
        except ValueError:
            self.search_fields.insert(0, 'subject_visit__appointment__registered_subject__identity')
        try:
            self.search_fields.index('subject_visit__appointment__registered_subject__first_name')
        except ValueError:
            self.search_fields.insert(0, 'subject_visit__appointment__registered_subject__first_name')
        try:
            self.search_fields.index('id')
        except ValueError:
            self.search_fields.insert(0, 'id')
        try:
            self.search_fields.index('subject_visit__subject_identifier')
        except ValueError:
            self.search_fields.insert(0, 'subject_visit__subject_identifier')

    def get_form_post(self, form, request, obj, **kwargs):
        NAME = 0
        WIDGET = 1
        form = super(SubjectVisitModelAdmin, self).get_form_post(form, request, obj, **kwargs)
        if form.optional_attrs:
            try:
                self.subject_visit = SubjectVisit.objects.get(pk=request.GET.get('subject_visit'))
                if self.subject_visit.appointment.visit_definition.code in ANNUAL_CODES:
                    for fld in form.base_fields.iteritems():
                        try:
                            fld[WIDGET].label = form.optional_attrs[ANNUAL]['label'][fld[NAME]]
                        except KeyError:
                            pass
                        try:
                            fld[WIDGET].help_text = form.optional_attrs[ANNUAL]['help_text'][fld[NAME]]
                        except KeyError:
                            pass
                        try:
                            fld[WIDGET].required = form.optional_attrs[ANNUAL]['required'][fld[NAME]]
                        except KeyError:
                            pass
            except SubjectVisit.DoesNotExist:
                pass
        return form

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
        Get a form Field for a ForeignKey based on the visit_code, baseline or annual.

        self.fields is already set
        """
        if self.fields == self.annual_fields:
            self.radio_fields = self.annual_radio_fields or self.radio_fields
        else:
            self.radio_fields = self.baseline_radio_fields or self.radio_fields
        return super(SubjectVisitModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def add_view(self, request, form_url='', extra_context=None):
        """Set the instructions based on the visit_code, baseline or annual."""
        try:
            self.subject_visit = SubjectVisit.objects.get(pk=request.GET.get('subject_visit'))
        except SubjectVisit.DoesNotExist:
            pass
#             subject_visit = SubjectVisit.objects.all()[0]
        if self.subject_visit and self.subject_visit.appointment.visit_definition.code in ANNUAL_CODES:
            self.fields = self.annual_fields
            self.instructions = self.annual_instructions or self.instructions
        else:
            self.fields = self.baseline_fields
            self.instructions = self.baseline_instructions or self.instructions
        return super(SubjectVisitModelAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """Set the instructions based on the visit_code, baseline or annual."""
        try:
            self.subject_visit = SubjectVisit.objects.get(pk=request.GET.get('subject_visit'))
        except SubjectVisit.DoesNotExist:
            pass
#             subject_visit = SubjectVisit.objects.all()[0]

        if self.subject_visit and self.subject_visit.appointment.visit_definition.code in ANNUAL_CODES:
            self.fields = self.annual_fields
            self.instructions = self.annual_instructions or self.instructions
        else:
            self.fields = self.baseline_fields
            self.instructions = self.baseline_instructions or self.instructions
        return super(SubjectVisitModelAdmin, self).change_view(request, object_id, form_url=form_url, extra_context=extra_context)

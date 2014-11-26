from edc.subject.visit_tracking.admin import BaseVisitTrackingModelAdmin

from apps.bcpp_survey.models import Survey

from ..models import SubjectVisit


class SubjectVisitModelAdmin (BaseVisitTrackingModelAdmin):

    """Model Admin for models with a foreignkey to the subject visit model."""

    visit_model = SubjectVisit
    visit_model_foreign_key = 'subject_visit'
    dashboard_type = 'subject'
    date_heirarchy = 'subject_visit__report_datetime'
    current_survey = Survey.objects.current_survey().survey_slug
    first_survey = Survey.objects.first_survey.survey_slug

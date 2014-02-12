from edc.subject.visit_tracking.admin import BaseVisitTrackingModelAdmin
from apps.bcpp_rbd_subject.models import SubjectVisitRBD


class SubjectVisitModelRBDAdmin (BaseVisitTrackingModelAdmin):

    """Model Admin for models with a foreignkey to the subject visit model."""

    visit_model = SubjectVisitRBD
    visit_model_foreign_key = 'subject_visit'
    dashboard_type = 'subject'
    date_heirarchy = 'subject_visit__report_datetime'

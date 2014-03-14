from edc.subject.visit_tracking.admin import BaseVisitTrackingModelAdmin

from ..models import RBDVisit


class RBDVisitModelAdmin (BaseVisitTrackingModelAdmin):

    """Model Admin for models with a foreignkey to the subject visit model."""

    visit_model = RBDVisit
    visit_model_foreign_key = 'subject_visit'
    dashboard_type = 'subject'
    date_heirarchy = 'subject_visit__report_datetime'

from edc.subject.visit_tracking.admin import BaseVisitTrackingModelAdmin
from ..models import HtcSubjectVisit


class HtcSubjectVisitModelAdmin (BaseVisitTrackingModelAdmin):

    """Model Admin for models with a foreignkey to the htc subject visit model."""

    visit_model = HtcSubjectVisit
    visit_attr = 'htc_subject_visit'
    dashboard_type = 'htc_subject'
    date_heirarchy = 'htc_subject_visit__report_datetime'

from bhp_visit_tracking.admin import BaseVisitTrackingModelAdmin
from bcpp_htc_subject.models import HtcSubjectVisit


class HtcSubjectVisitModelAdmin (BaseVisitTrackingModelAdmin):

    """Model Admin for models with a foreignkey to the htc subject visit model."""

    visit_model = HtcSubjectVisit
    visit_model_foreign_key = 'htc_subject_visit'
    dashboard_type = 'htc_subject'
    date_heirarchy = 'htc_subject_visit__report_datetime'

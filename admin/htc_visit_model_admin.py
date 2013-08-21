from bhp_visit_tracking.admin import BaseVisitTrackingModelAdmin
from bcpp_htc.models import HtcVisit


class HtcVisitModelAdmin (BaseVisitTrackingModelAdmin):

    """Model Admin for models with a foreignkey to the htc visit model."""

    visit_model = HtcVisit
    visit_model_foreign_key = 'htc_visit'
    dashboard_type = 'subject'
    date_heirarchy = 'htc_visit__report_datetime'

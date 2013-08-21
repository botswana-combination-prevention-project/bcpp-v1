from django.contrib import admin
from htc_visit_model_admin import HtcVisitModelAdmin
from bcpp_htc.models import HivResult
from bcpp_htc.forms import HivResultForm


class HivResultAdmin(HtcVisitModelAdmin):

    form = HivResultForm

    fields = (
        "todays_result",
        "circumcision_ap",
        "circumcision_ap_date",
        "couples_testing",
        "partner_id",
        "symptoms",
        "family_tb"
    )
    radio_fields = { 
        "circumcision_ap": admin.VERTICAL,
        "couples_testing": admin.VERTICAL, 
        "symptoms": admin.VERTICAL,
        "family_tb": admin.VERTICAL,      
        }

admin.site.register(HivResult, HivResultAdmin)

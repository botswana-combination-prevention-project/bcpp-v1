from django.contrib import admin
from htc_visit_model_admin import HtcVisitModelAdmin
from bcpp_htc.models import HivTestingCounseling
from bcpp_htc.forms import HivTestingCounselingForm


class HivTestingCounselingAdmin(HtcVisitModelAdmin):

    form = HivTestingCounselingForm

    fields = (
        "testing_today",
        "reason_not_testing",
        "todays_result",
        "cd4_test_date",
        "cd4_result",
        "clinic",
        "appointment_date",
        "circumcision_ap",
        "circumcision_ap_date",
        "couples_testing",
        "partner_id",
        "symptoms",
        "reffered_for",
        "reffered_to",
    )
    radio_fields = {
        "testing_today": admin.VERTICAL,
        "reason_not_testing": admin.VERTICAL, 
        "todays_result": admin.VERTICAL, 
        "todays_result": admin.VERTICAL,
        "circumcision_ap": admin.VERTICAL,
        "couples_testing": admin.VERTICAL,     
        
        }
    instructions = [("Request consent for HIV testing and counseling"
                     " from all age-eligible (16-64 years) clients who:"
                     " Do not have documentation of an HIV test within the last three months"
                     " Have documentation of HIV negative status within the last three months"
                     " and are pregnant Request to be tested")]

admin.site.register(HivTestingCounseling, HivTestingCounselingAdmin)

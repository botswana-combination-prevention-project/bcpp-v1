from django.contrib import admin
from htc_visit_model_admin import HtcVisitModelAdmin
from bcpp_htc.models import HivTestingConsent
from bcpp_htc.forms import HivTestingConsentForm


class HivTestingConsentAdmin(HtcVisitModelAdmin):

    form = HivTestingConsentForm

    fields = (
        "testing_today",
        "reason_not_testing",
    )
    radio_fields = {
        "testing_today": admin.VERTICAL,
        "reason_not_testing": admin.VERTICAL,      
        }
    instructions = [("Request consent for HIV testing and counseling"
                     " from all age-eligible (16-64 years) clients who:"
                     " Do not have documentation of an HIV test within the last three months"
                     " Have documentation of HIV negative status within the last three months"
                     " and are pregnant or those who request to be tested")]

admin.site.register(HivTestingConsent, HivTestingConsentAdmin)

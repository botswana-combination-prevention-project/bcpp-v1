from django.contrib import admin
from htc_visit_model_admin import HtcVisitModelAdmin
from bcpp_htc.models import PregnantFollowupConsent
from bcpp_htc.forms import PregnantFollowupConsentForm


class PregnantFollowupConsentAdmin(HtcVisitModelAdmin):

    form = PregnantFollowupConsentForm

    fields = (
      "contact_consent",
      "contact_family",
    )
    radio_fields = {
        "contact_permission": admin.VERTICAL,
        "contact_family": admin.VERTICAL,  
        }
    instructions = [("For women who are pregnant and HIV negative")]
admin.site.register(PregnantFollowupConsent, PregnantFollowupConsentAdmin)

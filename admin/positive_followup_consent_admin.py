from django.contrib import admin
from htc_visit_model_admin import HtcVisitModelAdmin
from bcpp_htc.models import PositiveFollowupConsent
from bcpp_htc.forms import PositiveFollowupConsentForm


class PositiveFollowupConsentAdmin(HtcVisitModelAdmin):

    form = PositiveFollowupConsentForm

    fields = (
      "contact_consent",
      "contact_family",
    )
    radio_fields = {
        "contact_consent": admin.VERTICAL,
        "contact_family": admin.VERTICAL,   
        }
    instructions = [("For newly identified HIV positive individuals and known"
                     " HIV positive individuals not enrolled in care")]
admin.site.register(PositiveFollowupConsent, PositiveFollowupConsentAdmin)

from django.contrib import admin
from htc_visit_model_admin import HtcVisitModelAdmin
from bcpp_htc.models import MaleFollowupConsent
from bcpp_htc.forms import MaleFollowupConsentForm


class MaleFollowupConsentAdmin(HtcVisitModelAdmin):

    form = MaleFollowupConsentForm

    fields = (
      "contact_consent",
      "contact_family",
    )
    radio_fields = {
        "contact_consent": admin.VERTICAL,
        "contact_family": admin.VERTICAL,   
        }
    instructions = [("For men who are HIV negative and uncircumcised")]
admin.site.register(MaleFollowupConsent, MaleFollowupConsentAdmin)

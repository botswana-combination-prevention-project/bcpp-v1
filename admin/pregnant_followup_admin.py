from django.contrib import admin
from htc_subject_visit_model_admin import HtcSubjectVisitModelAdmin
from bcpp_htc_subject.models import PregnantFollowup
from bcpp_htc_subject.forms import PregnantFollowupForm


class PregnantFollowupAdmin(HtcSubjectVisitModelAdmin):

    form = PregnantFollowupForm

    fields = (
    "htc_subject_visit",
      "contact_consent",
      "contact_family",
    )
    radio_fields = {
        "contact_consent": admin.VERTICAL,
        "contact_family": admin.VERTICAL,
        }
    instructions = [("For women who are pregnant and HIV negative")]
admin.site.register(PregnantFollowup, PregnantFollowupAdmin)

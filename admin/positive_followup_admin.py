from django.contrib import admin
from htc_subject_visit_model_admin import HtcSubjectVisitModelAdmin
from bcpp_subject_htc.models import PositiveFollowup
from bcpp_subject_htc.forms import PositiveFollowupForm


class PositiveFollowupAdmin(HtcSubjectVisitModelAdmin):

    form = PositiveFollowupForm

    fields = (
        "htc_subject_visit",
      "contact_consent",
      "contact_family",
    )
    radio_fields = {
        "contact_consent": admin.VERTICAL,
        "contact_family": admin.VERTICAL,
        }
    instructions = [("For newly identified HIV positive individuals and known"
                     " HIV positive individuals not enrolled in care")]
admin.site.register(PositiveFollowup, PositiveFollowupAdmin)

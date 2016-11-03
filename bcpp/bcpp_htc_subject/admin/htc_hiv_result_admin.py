from django.contrib import admin
from htc_subject_visit_model_admin import HtcSubjectVisitModelAdmin
from ..models import HtcHivResult
from ..forms import HtcHivResultForm


class HtcHivResultAdmin(HtcSubjectVisitModelAdmin):

    form = HtcHivResultForm

    fields = (
        "htc_subject_visit",
        "todays_result",
        "couples_testing",
        "partner_id",
        "symptoms",
        "family_tb"
    )
    radio_fields = {
        "couples_testing": admin.VERTICAL,
        "symptoms": admin.VERTICAL,
        "family_tb": admin.VERTICAL,
    }
admin.site.register(HtcHivResult, HtcHivResultAdmin)

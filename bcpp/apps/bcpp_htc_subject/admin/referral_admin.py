from django.contrib import admin
from htc_subject_visit_model_admin import HtcSubjectVisitModelAdmin
from ..models import Referral
from ..forms import ReferralForm


class ReferralAdmin(HtcSubjectVisitModelAdmin):

    form = ReferralForm

    fields = (
        "htc_subject_visit",
        "referred_for",
        "referred_to",
    )
admin.site.register(Referral, ReferralAdmin)

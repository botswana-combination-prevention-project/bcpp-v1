from django.contrib import admin
from htc_subject_visit_model_admin import HtcSubjectVisitModelAdmin
from bcpp_htc.models import Referral
from bcpp_htc.forms import ReferralForm


class ReferralAdmin(HtcSubjectVisitModelAdmin):

    form = ReferralForm

    fields = (
        "referred_for",
        "referred_to",
    )

admin.site.register(Referral, ReferralAdmin)

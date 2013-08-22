from django.contrib import admin
from htc_visit_model_admin import HtcVisitModelAdmin
from bcpp_htc.models import Cd4Test
from bcpp_htc.forms import Cd4TestForm


class Cd4TestAdmin(HtcVisitModelAdmin):

    form = Cd4TestForm

    fields = (
        "cd4_test_date",
        "cd4_result",
        "referral_clinic",
        "appointment_date",
    )

admin.site.register(Cd4Test, Cd4TestAdmin)

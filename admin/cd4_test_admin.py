from django.contrib import admin
from htc_visit_model_admin import HtcVisitModelAdmin
from bcpp_htc.models import CD4Test
from bcpp_htc.forms import CD4TestForm


class CD4TestAdmin(HtcVisitModelAdmin):

    form = CD4TestForm

    fields = (
        "cd4_test_date",
        "cd4_result",
        "referral_clinic",
        "appointment_date",
    )

admin.site.register(CD4Test, CD4TestAdmin)

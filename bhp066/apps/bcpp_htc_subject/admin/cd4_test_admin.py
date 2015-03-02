from django.contrib import admin
from ..models import Cd4Test
from ..forms import Cd4TestForm
from .htc_subject_visit_model_admin import HtcSubjectVisitModelAdmin


class Cd4TestAdmin(HtcSubjectVisitModelAdmin):

    form = Cd4TestForm

    fields = (
        "htc_subject_visit",
        "cd4_test_date",
        "cd4_result",
        "referral_clinic",
        "appointment_date",
    )

admin.site.register(Cd4Test, Cd4TestAdmin)

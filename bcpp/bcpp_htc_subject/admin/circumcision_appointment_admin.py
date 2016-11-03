from django.contrib import admin
from ..models import CircumcisionAppointment
from ..forms import CircumcisionAppointmentForm
from .htc_subject_visit_model_admin import HtcSubjectVisitModelAdmin


class CircumcisionAppointmentAdmin(HtcSubjectVisitModelAdmin):

    form = CircumcisionAppointmentForm

    fields = (
        "htc_subject_visit",
        "circumcision_ap",
        "circumcision_ap_date",
    )
    radio_fields = {
        "circumcision_ap": admin.VERTICAL,
    }
    instructions = [("For male negative and uncircumcised")]

admin.site.register(CircumcisionAppointment, CircumcisionAppointmentAdmin)

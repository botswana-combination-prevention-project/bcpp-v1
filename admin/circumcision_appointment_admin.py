from django.contrib import admin
from htc_subject_visit_model_admin import HtcSubjectVisitModelAdmin
from bcpp_subject_htc.models import CircumcisionAppointment
from bcpp_subject_htc.forms import CircumcisionAppointmentForm


class CircumcisionAppointmentAdmin(HtcSubjectVisitModelAdmin):

    form = CircumcisionAppointmentForm

    fields = (
        "circumcision_ap",
        "circumcision_ap_date",
    )
    radio_fields = {
        "circumcision_ap": admin.VERTICAL,
        }
    instructions = [("For male negative and uncircumcised")]

admin.site.register(CircumcisionAppointment, CircumcisionAppointmentAdmin)

from django.contrib import admin
from htc_visit_model_admin import HtcVisitModelAdmin
from bcpp_htc.models import CircumcisionAppointment
from bcpp_htc.forms import CircumcisionAppointmentForm


class CircumcisionAppointmentAdmin(HtcVisitModelAdmin):

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

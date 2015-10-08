from django.contrib import admin
from django.utils.translation import ugettext as _

from ..models import HospitalAdmission
from ..forms import HospitalAdmissionForm

from .subject_visit_model_admin import SubjectVisitModelAdmin


class HospitalAdmissionAdmin(SubjectVisitModelAdmin):

    form = HospitalAdmissionForm
    fields = (
        "subject_visit",
        "admission_nights",
        "reason_hospitalized",
        "facility_hospitalized",
        "nights_hospitalized",
        "healthcare_expense",
        "travel_hours",
        "total_expenses",
        "hospitalization_costs",
    )
    radio_fields = {
        "reason_hospitalized": admin.VERTICAL,
        "travel_hours": admin.VERTICAL,
        "hospitalization_costs": admin.VERTICAL,
    }
    instructions = [
        _("<H5>Read to Participant</H5> Read to Participant: For the next set of questions please "
          "think about times you were admitted to a hospital in the last 3 months")]
admin.site.register(HospitalAdmission, HospitalAdmissionAdmin)

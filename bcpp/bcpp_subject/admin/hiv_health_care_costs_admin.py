from django.contrib import admin

from ..forms import HivHealthCareCostsForm
from ..models import HivHealthCareCosts

from .subject_visit_model_admin import SubjectVisitModelAdmin


class HivHealthCareCostsAdmin(SubjectVisitModelAdmin):

    form = HivHealthCareCostsForm
    fields = (
        "subject_visit",
        "hiv_medical_care",
        "reason_no_care",
        "place_care_received",
        "care_regularity",
        "doctor_visits",
    )
    radio_fields = {
        "hiv_medical_care": admin.VERTICAL,
        "reason_no_care": admin.VERTICAL,
        "place_care_received": admin.VERTICAL,
        "care_regularity": admin.VERTICAL,
        "doctor_visits": admin.VERTICAL,
    }
admin.site.register(HivHealthCareCosts, HivHealthCareCostsAdmin)

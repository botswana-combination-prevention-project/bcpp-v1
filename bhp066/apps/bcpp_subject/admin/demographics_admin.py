from django.contrib import admin

from ..forms import DemographicsForm
from ..models import Demographics

from .subject_visit_model_admin import SubjectVisitModelAdmin


class DemographicsAdmin(SubjectVisitModelAdmin):

    form = DemographicsForm

    fields = [
        "subject_visit",
        'religion',
        'religion_other',
        'ethnic',
        'ethnic_other',
        'marital_status',
        'num_wives',
        'husband_wives',
        'live_with',
        ]

    annual_fields = [f for f in fields if f not in ['religion', 'religion_other', 'ethnic', 'ethnic_other']]

    radio_fields = {
        "marital_status": admin.VERTICAL, }
    filter_horizontal = ('live_with', 'religion', 'ethnic')


admin.site.register(Demographics, DemographicsAdmin)

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
    radio_fields = {
        "marital_status": admin.VERTICAL, }
    filter_horizontal = ('live_with', 'religion', 'ethnic')

if DemographicsAdmin.current_survey != DemographicsAdmin.first_survey:
    DemographicsAdmin.fields.remove('religion')
    DemographicsAdmin.fields.remove('religion_other')
    DemographicsAdmin.fields.remove('ethnic')
    DemographicsAdmin.fields.remove('ethnic_other')

admin.site.register(Demographics, DemographicsAdmin)

from django.contrib import admin

from ..forms import RbdDemographicsForm
from ..models import RbdDemographics

from .subject_visit_model_admin import SubjectVisitModelAdmin


class RbdDemographicsAdmin(SubjectVisitModelAdmin):

    form = RbdDemographicsForm
    fields = (
        "subject_visit",
        'religion',
        'religion_other',
        'ethnic',
        'ethnic_other',
        'marital_status',
        'num_wives',
        'husband_wives',
        'live_with',)
    radio_fields = {
        "marital_status": admin.VERTICAL, }
    filter_horizontal = ('live_with', 'religion', 'ethnic')
admin.site.register(RbdDemographics, RbdDemographicsAdmin)

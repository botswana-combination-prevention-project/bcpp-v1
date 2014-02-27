from django.contrib import admin
from ..models import RBDDemographics
from ..forms import RBDDemographicsForm
from .subject_visit_model_rbd_admin import SubjectVisitModelRBDAdmin


class RBDDemographicsAdmin(SubjectVisitModelRBDAdmin):

    form = RBDDemographicsForm
    fields = (
        "subject_visit_rbd",
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
admin.site.register(RBDDemographics, RBDDemographicsAdmin)

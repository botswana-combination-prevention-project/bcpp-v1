from django.contrib import admin

from ..forms import RBDDemographicsForm
from ..models import RBDDemographics

from .rbd_visit_model_admin import RBDVisitModelAdmin


class RBDDemographicsAdmin(RBDVisitModelAdmin):

    form = RBDDemographicsForm
    fields = (
        "rbd_visit",
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

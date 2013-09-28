from django.contrib import admin
from bcpp_subject.models import Demographics
from bcpp_subject.forms import DemographicsForm
from subject_visit_model_admin import SubjectVisitModelAdmin


class DemographicsAdmin(SubjectVisitModelAdmin):

    form = DemographicsForm
    fields = (
        "subject_visit",
        'religion',
        'religion_other',
        'ethnic',
        'other',
        'marital_status',
        'num_wives',
        'husband_wives',
        'live_with',)
    radio_fields = {
        "marital_status": admin.VERTICAL, }
    filter_horizontal = ('live_with', 'religion', 'ethnic')
admin.site.register(Demographics, DemographicsAdmin)

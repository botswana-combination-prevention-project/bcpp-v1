from django.contrib import admin
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import Demographics
from bcpp_subject.forms import DemographicsForm


class DemographicsAdmin(SubjectVisitModelAdmin):

    form = DemographicsForm
    fields = (
        "subject_visit",
        'religion',
        'ethnic',
        'marital_status',
        'num_wives',
        'husband_wives',
        'live_with',)
    radio_fields = {
        "marital_status": admin.VERTICAL, }
    filter_horizontal = ('live_with','religion')
admin.site.register(Demographics, DemographicsAdmin)

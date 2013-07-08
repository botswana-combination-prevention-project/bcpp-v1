from django.contrib import admin
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import SexualBehaviour
from bcpp_subject.forms import SexualBehaviourForm


class SexualBehaviourAdmin(SubjectVisitModelAdmin):

    form = SexualBehaviourForm
    fields = (
        "subject_visit",
        'ever_sex',
        'last_year_partners',
        'more_sex',
        'first_sex',
        'condom',
        'alcohol_sex',
        'last_sex',
        'last_sex_calc',)
    radio_fields = {
        "ever_sex": admin.VERTICAL,
        "more_sex": admin.VERTICAL,
        "condom": admin.VERTICAL,
        "alcohol_sex": admin.VERTICAL,
        "last_sex": admin.VERTICAL, }
admin.site.register(SexualBehaviour, SexualBehaviourAdmin)

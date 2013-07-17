from django.contrib import admin
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import NonPregnancy
from bcpp_subject.forms import NonPregnancyForm


class NonPregnancyAdmin(SubjectVisitModelAdmin):

    form = NonPregnancyForm
    fields = (
        "subject_visit",
        'more_children',
        'last_birth',
        'anc_last_pregnancy',
        'hiv_last_pregnancy',
        'preg_arv',)
    radio_fields = {
        "more_children": admin.VERTICAL,
        "anc_last_pregnancy": admin.VERTICAL,
        "hiv_last_pregnancy": admin.VERTICAL,
        "preg_arv": admin.VERTICAL, }
admin.site.register(NonPregnancy, NonPregnancyAdmin)

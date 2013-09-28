from django.contrib import admin
from edc_lib.bhp_supplemental_fields.classes import SupplementalFields
from bcpp_subject.models import HivUntested
from bcpp_subject.forms import HivUntestedForm
from subject_visit_model_admin import SubjectVisitModelAdmin


#HIV testing and history [HT]: 10% in pretest, 9% in BHS and all follow-up
class HivUntestedAdmin(SubjectVisitModelAdmin):

    form = HivUntestedForm
    supplemental_fields = SupplementalFields(
        ('why_no_hiv_test',
        'hiv_pills',
        'arvs_hiv_test'), p=0.09, group='HT')
    fields = (
        "subject_visit",
        'why_no_hiv_test',
        'hiv_pills',
        'arvs_hiv_test',)
    radio_fields = {
        "why_no_hiv_test": admin.VERTICAL,
        "hiv_pills": admin.VERTICAL,
        "arvs_hiv_test": admin.VERTICAL, }
admin.site.register(HivUntested, HivUntestedAdmin)

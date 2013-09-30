from django.contrib import admin
from edc.core.bhp_supplemental_fields.classes import SupplementalFields
from ..models import HivTested
from ..forms import HivTestedForm
from .subject_visit_model_admin import SubjectVisitModelAdmin


#HIV testing and history [HT]: 10% in pretest, 9% in BHS and all follow-up
class HivTestedAdmin(SubjectVisitModelAdmin):

    form = HivTestedForm
    supplemental_fields = SupplementalFields(
        ('num_hiv_tests',
        'why_hiv_test',
        'hiv_pills',
        'arvs_hiv_test'), p=0.09, group='HT')
    fields = (
        "subject_visit",
        'num_hiv_tests',
        'where_hiv_test',
        'where_hiv_test_other',
        'why_hiv_test',
        'hiv_pills',
        'arvs_hiv_test',)
    radio_fields = {
        "where_hiv_test": admin.VERTICAL,
        "why_hiv_test": admin.VERTICAL,
        "hiv_pills": admin.VERTICAL,
        "arvs_hiv_test": admin.VERTICAL, }
admin.site.register(HivTested, HivTestedAdmin)

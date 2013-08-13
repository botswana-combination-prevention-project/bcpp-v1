from django.contrib import admin
# from bhp_supplemental_fields.classes import SupplementalFields
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import HivTested
from bcpp_subject.forms import HivTestedForm


class HivTestedAdmin(SubjectVisitModelAdmin):

    form = HivTestedForm
#     supplemental_fields = SupplementalFields(
#         ('num_hiv_tests',
#         'why_hiv_test',
#         'hiv_pills',
#         'arvs_hiv_test'), p=0.09, group='HT')
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

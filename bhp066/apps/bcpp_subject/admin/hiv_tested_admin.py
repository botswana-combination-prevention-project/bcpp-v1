from django.contrib import admin

from ..forms import HivTestedForm
from ..models import HivTested

from .subject_visit_model_admin import SubjectVisitModelAdmin


# HIV testing and history [HT]: 10% in pretest, 9% in BHS and all follow-up
class HivTestedAdmin(SubjectVisitModelAdmin):

    form = HivTestedForm
    baseline_fields = [
        "subject_visit",
        'num_hiv_tests',
        'where_hiv_test',
        'where_hiv_test_other',
        'why_hiv_test',
        'hiv_pills',
        'arvs_hiv_test']
    annual_fields = [f for f in baseline_fields if f not in ['num_hiv_tests', 'hiv_pills', 'arvs_hiv_test', 'why_hiv_test']]
    baseline_radio_fields = {
        "where_hiv_test": admin.VERTICAL,
        "why_hiv_test": admin.VERTICAL,
        "hiv_pills": admin.VERTICAL,
        "arvs_hiv_test": admin.VERTICAL, }
    annual_radio_fields = {
        "where_hiv_test": admin.VERTICAL,
        "why_hiv_test": admin.VERTICAL}

admin.site.register(HivTested, HivTestedAdmin)

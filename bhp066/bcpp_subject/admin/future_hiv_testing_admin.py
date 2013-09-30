from django.contrib import admin
from edc.core.admin_supplemental_fields.classes import SupplementalFields
from ..models import FutureHivTesting
from ..forms import FutureHivTestingForm
from .subject_visit_model_admin import SubjectVisitModelAdmin


#HIV testing and history [HT]: 10% in pretest, 9% in BHS and all follow-up
class FutureHivTestingAdmin(SubjectVisitModelAdmin):

    form = FutureHivTestingForm
    supplemental_fields = SupplementalFields(
        ('prefer_hivtest',
        'hiv_test_time',
        'hiv_test_time_other',
        'hiv_test_week',
        'hiv_test_week_other',
        'hiv_test_year',
        'hiv_test_year_other',), p=0.09, group='HT')
    fields = (
        "subject_visit",
        'prefer_hivtest',
        'hiv_test_time',
        'hiv_test_time_other',
        'hiv_test_week',
        'hiv_test_week_other',
        'hiv_test_year',
        'hiv_test_year_other')
    radio_fields = {
        'prefer_hivtest': admin.VERTICAL,
        "hiv_test_time": admin.VERTICAL,
        "hiv_test_week": admin.VERTICAL,
        "hiv_test_year": admin.VERTICAL, }
    instructions = [("Note to Interviewer: This form is only for HIV- (negative) participants"),
                  ("Read to Participant: The following questions are "
                  "about how you would like to have HIV testing in the future.")]
admin.site.register(FutureHivTesting, FutureHivTestingAdmin)

from django.contrib import admin
# from bhp_supplemental_fields.classes import SupplementalFields
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import FutureHivTesting
from bcpp_subject.forms import FutureHivTestingForm


class FutureHivTestingAdmin(SubjectVisitModelAdmin):

    form = FutureHivTestingForm
#     supplemental_fields = SupplementalFields(
#         ('prefer_hivtest',
#         'hiv_test_time',
#         'hiv_test_time_other',
#         'hiv_test_week',
#         'hiv_test_week_other',
#         'hiv_test_year',
#         'hiv_test_year_other',), p=0.09, group='HT')
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

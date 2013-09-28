from django.contrib import admin
from bcpp_subject.models import HivTestReview
from bcpp_subject.forms import HivTestReviewForm
from subject_visit_model_admin import SubjectVisitModelAdmin


class HivTestReviewAdmin(SubjectVisitModelAdmin):

    form = HivTestReviewForm
    fields = (
        "subject_visit",
        'hiv_test_date',
        'recorded_hiv_result')
    radio_fields = {
        "recorded_hiv_result": admin.VERTICAL, }
admin.site.register(HivTestReview, HivTestReviewAdmin)

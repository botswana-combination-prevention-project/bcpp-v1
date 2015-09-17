from django.contrib import admin

from ..forms import HivTestReviewForm
from ..models import HivTestReview

from .subject_visit_model_admin import SubjectVisitModelAdmin


class HivTestReviewAdmin(SubjectVisitModelAdmin):

    form = HivTestReviewForm
    fields = (
        "subject_visit",
        'hiv_test_date',
        'recorded_hiv_result')
    radio_fields = {
        "recorded_hiv_result": admin.VERTICAL, }
admin.site.register(HivTestReview, HivTestReviewAdmin)

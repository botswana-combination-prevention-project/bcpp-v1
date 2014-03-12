from django.contrib import admin
from ..models import  HicEnrollment
from ..forms import HicEnrollmentForm
from .subject_visit_model_admin import SubjectVisitModelAdmin


class HicEnrollmentAdmin(SubjectVisitModelAdmin):

    form = HicEnrollmentForm
    fields = (
        "subject_visit",
        "hic_permission"
        )
admin.site.register(HicEnrollment, HicEnrollmentAdmin)

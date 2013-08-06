from django.contrib import admin
from subject_visit_model_admin import SubjectVisitModelAdmin
from bcpp_subject.models import Education
from bcpp_subject.forms import EducationForm


class EducationAdmin(SubjectVisitModelAdmin):

    form = EducationForm
    fields = (
        "subject_visit",
        'education',
        'working',
        'job_type',
        'reason_unemployed',
        'job_description',
        'monthly_income',)
    radio_fields = {
        "education": admin.VERTICAL,
        "working": admin.VERTICAL,
        'job_type': admin.VERTICAL,
        'reason_unemployed': admin.VERTICAL,
        'job_description': admin.VERTICAL,
        "monthly_income": admin.VERTICAL, }
    required_instructions = ("Read to Participant: Next, I will ask you some"
                              " questions about what education and work you"
                              " may have done or are currently doing.")
admin.site.register(Education, EducationAdmin)

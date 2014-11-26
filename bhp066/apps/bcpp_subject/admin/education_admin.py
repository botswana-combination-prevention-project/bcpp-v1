from django.contrib import admin
from django.utils.translation import ugettext as _

from ..models import Education
from ..forms import EducationForm
from .subject_visit_model_admin import SubjectVisitModelAdmin


class EducationAdmin(SubjectVisitModelAdmin):

    form = EducationForm
    fields = [
        "subject_visit",
        'education',
        'working',
        'job_type',
        'reason_unemployed',
        'job_description',
        'monthly_income']
    radio_fields = {
        "education": admin.VERTICAL,
        "working": admin.VERTICAL,
        'job_type': admin.VERTICAL,
        'reason_unemployed': admin.VERTICAL,
        'job_description': admin.VERTICAL,
        "monthly_income": admin.VERTICAL, }
    instructions = [_("Read to Participant: Next, I will ask you some "
                      "questions about what education and work you "
                      "may have done or are currently doing.")]

if EducationAdmin.current_survey != EducationAdmin.first_survey:
    EducationAdmin.fields.remove('education')
    del EducationAdmin.radio_fields['education']
    EducationAdmin.fields.remove('working')
    del EducationAdmin.radio_fields['working']
    EducationAdmin.fields.remove('job_type')
    del EducationAdmin.radio_fields['job_type']
    EducationAdmin.fields.remove('reason_unemployed')
    del EducationAdmin.radio_fields['reason_unemployed']
admin.site.register(Education, EducationAdmin)

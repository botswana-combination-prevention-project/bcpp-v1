from django.contrib import admin
from django.utils.translation import ugettext as _

from ..constants import ANNUAL
from ..forms import EducationForm
from ..models import Education

from .subject_admin_exclude_mixin import SubjectAdminExcludeMixin
from .subject_visit_model_admin import SubjectVisitModelAdmin


class EducationAdmin(SubjectAdminExcludeMixin, SubjectVisitModelAdmin):

    form = EducationForm

    fields = [
        "subject_visit",
        'education',
        'working',
        'job_type',
        'reason_unemployed',
        'job_description',
        'monthly_income']

    custom_exclude = {
        ANNUAL: [
            'education',
            'working',
            'job_type',
            'reason_unemployed']
    }

    radio_fields = {
        "education": admin.VERTICAL,
        "working": admin.VERTICAL,
        'job_type': admin.VERTICAL,
        'reason_unemployed': admin.VERTICAL,
        'job_description': admin.VERTICAL,
        "monthly_income": admin.VERTICAL,
        'job_description': admin.VERTICAL,
        "monthly_income": admin.VERTICAL, }


#     baseline_fields = (
#         "subject_visit",
#         'education',
#         'working',
#         'job_type',
#         'reason_unemployed',
#         'job_description',
#         'monthly_income')
#
#     annual_fields = (
#         "subject_visit",
#         'job_description',
#         'monthly_income')
#
#     baseline_radio_fields = {
#         "education": admin.VERTICAL,
#         "working": admin.VERTICAL,
#         'job_type': admin.VERTICAL,
#         'reason_unemployed': admin.VERTICAL,
#         'job_description': admin.VERTICAL,
#         "monthly_income": admin.VERTICAL, }
#
#     annual_radio_fields = {
#         'job_description': admin.VERTICAL,
#         "monthly_income": admin.VERTICAL, }

    instructions = [_("<H5>Read to Participant</H5> Next, I will ask you some "
                      "questions about what education and work you "
                      "may have done or are currently doing.")]

admin.site.register(Education, EducationAdmin)

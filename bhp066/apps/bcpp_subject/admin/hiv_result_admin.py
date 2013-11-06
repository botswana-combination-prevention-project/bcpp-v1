from django.contrib import admin
from ..models import HivResult
from ..forms import HivResultForm
from .subject_visit_model_admin import SubjectVisitModelAdmin


class HivResultAdmin (SubjectVisitModelAdmin):

    form = HivResultForm
    fields = (
        'subject_visit',
        'hiv_result',
        'hiv_result_datetime',
        'why_not_tested',)
    radio_fields = {
        "hiv_result": admin.VERTICAL,
        'why_not_tested': admin.VERTICAL, }
    instructions = [("This section collects information on whether or not the"
                     "participant has either:"
                     "a) documentation of an HIV test result other than the"
                     " most recent HIV test (positive, negative, or "
                     "indeterminate); OR "
                     "b) documentation that supports a previous diagnosis of"
                     " HIV, if record of positive HIV test is not available. "),]
admin.site.register(HivResult, HivResultAdmin)

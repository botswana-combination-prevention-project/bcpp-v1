from django.contrib import admin
from ..models import HivResultDocumentation
from ..forms import HivResultDocumentationForm
from .subject_visit_model_admin import SubjectVisitModelAdmin


class HivResultDocumentationAdmin (SubjectVisitModelAdmin):

    form = HivResultDocumentationForm
    fields = (
        'subject_visit',
        'result_date',
        'result_doc_type',)
    radio_fields = {
        'result_doc_type': admin.VERTICAL, }
    instructions = [("This section collects information on whether or not the"
                     " participant has either:"
                     " a) documentation of an HIV test result other than the"
                     " most recent HIV test (positive, negative, or "
                     " indeterminate); OR "
                     " b) documentation that supports a previous diagnosis of"
                     " HIV, if record of positive HIV test is not available. "),]
admin.site.register(HivResultDocumentation, HivResultDocumentationAdmin)

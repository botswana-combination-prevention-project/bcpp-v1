from django.contrib import admin

from ..forms import HivResultDocumentationForm
from ..models import HivResultDocumentation

from .subject_visit_model_admin import SubjectVisitModelAdmin


class HivResultDocumentationAdmin (SubjectVisitModelAdmin):

    form = HivResultDocumentationForm
    fields = (
        'subject_visit',
        'result_date',
        'result_doc_type',)
    radio_fields = {
        'result_doc_type': admin.VERTICAL, }

    baseline_instructions = [
        ("This section collects information on whether or not the"
         " participant has either:"
         " <ol><li>documentation of an HIV test result other than the"
         " most recent HIV test (positive, negative, or "
         " indeterminate) ; OR </li>"
         " <li> documentation that supports a previous diagnosis of"
         " HIV, if record of positive HIV test is not available.</li></ol> ")
    ]

    annual_instructions = [
        ("This section collects information on whether or not the"
         " participant has either:"
         " <ol><li>documentation of an HIV test result other than the"
         " most recent HIV test; OR</li>"
         " <li>documentation that supports a previous diagnosis of"
         " HIV, if record of positive HIV test is not available.</li></ol>")
    ]

admin.site.register(HivResultDocumentation, HivResultDocumentationAdmin)

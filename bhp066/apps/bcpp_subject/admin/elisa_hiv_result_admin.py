from django.contrib import admin

from ..forms import ElisaHivResultForm
from ..models import ElisaHivResult
from ..filters import HivResultFilter

from .subject_visit_model_admin import SubjectVisitModelAdmin


class ElisaHivResultAdmin (SubjectVisitModelAdmin):

    form = ElisaHivResultForm
    fields = (
        'subject_visit',
        'hiv_result',
        'hiv_result_datetime',
    )

    list_filter = (HivResultFilter,)

    radio_fields = {
        "hiv_result": admin.VERTICAL,
    }
admin.site.register(ElisaHivResult, ElisaHivResultAdmin)

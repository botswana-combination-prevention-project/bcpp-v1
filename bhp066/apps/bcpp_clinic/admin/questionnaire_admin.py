from django.contrib import admin

from ..filters import ClinicCommunityListFilter
from ..forms import QuestionnaireForm
from ..models import Questionnaire

from .clinic_visit_model_admin import ClinicVisitModelAdmin


class QuestionnaireAdmin(ClinicVisitModelAdmin):

    form = QuestionnaireForm
    fields = (
        "clinic_visit",
        "report_datetime",
        "on_arv",
        "knows_last_cd4",
        "cd4_count",
    )
    radio_fields = {
        "on_arv": admin.VERTICAL,
        "knows_last_cd4": admin.VERTICAL,
        }
    list_display = ('clinic_visit', 'on_arv', 'cd4_count', 'report_datetime')
    list_filter = ('on_arv', ClinicCommunityListFilter, 'report_datetime')
    search_fields = ('on_arv',)
admin.site.register(Questionnaire, QuestionnaireAdmin)

from django.contrib import admin
from edc.base.modeladmin.admin import BaseModelAdmin
from ..models import Survey


class SurveyAdmin (BaseModelAdmin):

    list_display = ('survey_name', 'chronological_order',
                    'datetime_start', 'datetime_end')

admin.site.register(Survey, SurveyAdmin)

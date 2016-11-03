from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..models import Survey


class SurveyAdmin (BaseModelAdmin):

    list_display = ('survey_name', 'survey_abbrev', 'chronological_order',
                    'datetime_start', 'datetime_end')

admin.site.register(Survey, SurveyAdmin)

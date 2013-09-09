from django.contrib import admin
from bhp_base_admin.admin import BaseModelAdmin
from bcpp_survey.models import Survey


class SurveyAdmin (BaseModelAdmin):

    list_display = ('survey_name', 'chronological_order',
                    'datetime_start', 'datetime_end')

admin.site.register(Survey, SurveyAdmin)

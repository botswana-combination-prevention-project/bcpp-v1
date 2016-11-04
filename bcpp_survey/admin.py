from django.contrib import admin

from edc_base.modeladmin.mixins import ModelAdminBasicMixin

from .models import Survey


class SurveyAdmin (ModelAdminBasicMixin):

    list_display = ('survey_name', 'survey_abbrev', 'chronological_order',
                    'datetime_start', 'datetime_end')

admin.site.register(Survey, SurveyAdmin)

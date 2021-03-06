from django.contrib import admin

from edc_base.modeladmin.mixins import ModelAdminBasicMixin

from .models import Survey
from .admin_site import bcpp_survey_admin


@admin.register(Survey, site=bcpp_survey_admin)
class SurveyAdmin (ModelAdminBasicMixin, admin.ModelAdmin):

    list_display = ('survey_name', 'survey_abbrev', 'chronological_order',
                    'datetime_start', 'datetime_end')

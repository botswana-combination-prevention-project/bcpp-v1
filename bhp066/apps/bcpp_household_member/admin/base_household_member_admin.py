from edc.base.modeladmin.admin import BaseModelAdmin

from bhp066.apps.bcpp_survey.models import Survey


class BaseHouseholdMemberAdmin(BaseModelAdmin):

    current_survey = Survey.objects.current_survey().survey_slug

    first_survey = Survey.objects.first_survey.survey_slug

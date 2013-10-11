from datetime import datetime
from django.db import models


class SurveyManager(models.Manager):

    def get_by_natural_key(self, survey_name):
        return self.get(survey_name=survey_name)

    def current_survey(self):
        """Returns the instance of the current survey based on today's date or None."""
        current_survey = None
        if super(SurveyManager, self).filter(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today()).count() == 1:
            current_survey = super(SurveyManager, self).get(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today())
        return current_survey

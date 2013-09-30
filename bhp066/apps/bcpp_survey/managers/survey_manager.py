from django.db import models


class SurveyManager(models.Manager):

    def get_by_natural_key(self, survey_name):
        return self.get(survey_name=survey_name)

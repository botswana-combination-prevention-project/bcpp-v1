from django.db import models


class HouseholdSurveyManager(models.Manager):

    def get_by_natural_key(self, household, survey_code):
        return self.get(household=household, survey_code=survey_code, )

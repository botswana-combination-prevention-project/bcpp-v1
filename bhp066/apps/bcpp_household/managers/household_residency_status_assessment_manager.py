from django.db import models


class HouseholdResidencyStatusAssessmentManager(models.Manager):

    def natural_key(self):
        return self.household.natural_key() + self.survey.natural_key()
    natural_key.dependencies = ['bcpp_household.household']

from django.db import models
from bcpp_household.managers import HouseholdSurveyManager
from base_uuid_model import BaseUuidModel
from bcpp_list.models import HouseholdSurveyCode
from household import Household


class HouseholdSurvey(BaseUuidModel):

    household = models.ForeignKey(Household)

    survey_code = models.ForeignKey(HouseholdSurveyCode)

    contact_name = models.CharField("Contact Name",
        max_length=100,
        blank=True,
        help_text="Not required, but useful if rescheduling"
        )

    contact_tel = models.CharField("Contact Tel",
        max_length=25,
        blank=True,
        help_text="Not required, but useful if rescheduling"
        )

    comment = models.CharField("Additional Comments",
        max_length=250,
        blank=True
        )
    objects = HouseholdSurveyManager()

    def natural_key(self):
        return self.household.natural_key() + self.survey_code.natural_key()

    def __unicode__(self):
        return "%s %s" % (self.household, self.survey_code)

    def get_absolute_url(self):
        return "/bcpp_household/householdsurvey/%s/" % self.id

    def calendar_datetime(self):
        return self.created

    def calendar_label(self):
        return self.__unicode__()

    def calendar_absolute_url(self):
        return self.household.householdstructure.get_absolute_url()

    def get_url(self):
        return "/bcpp_household/householdsurvey/"

    class Meta:
        unique_together = (("household", "survey_code"),)
        app_label = 'bcpp_household'
        db_table = 'bcpp_householdsurvey'

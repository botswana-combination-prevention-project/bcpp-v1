from django.db import models
from django.utils.translation import ugettext_lazy as _
from household_survey import HouseholdSurvey
from bcpp_list.models import HouseholdSurveyStatus
from base_uuid_model import BaseUuidModel


class HouseholdSurveyReport(BaseUuidModel):
    household_survey = models.ForeignKey(HouseholdSurvey,
        )
    survey_date = models.DateField(
        verbose_name=_("Survey Date"),
        help_text=_("Date format is YYYY-MM-DD"),
        )
    survey_start_time = models.TimeField(
        verbose_name=_("Survey Start Time"),
        help_text=_("Time format is HH:MM"),
        )
    survey_end_time = models.TimeField(
        verbose_name=_("Survey Finish Time"),
        help_text=_('If the survey is \'IN PROGRESS\' now, you may leave this blank. '
                    'Time format is HH:MM'),
        null=True,
        blank=True,
        )
    household_survey_status = models.ForeignKey(HouseholdSurveyStatus,
        verbose_name=_("Survey Status"),
        )
    comment = models.CharField(
        verbose_name=_("Comment"),
        max_length=250,
        blank=True
        )

    def __unicode__(self):
        return unicode(self.household_survey)

    def get_absolute_url(self):
        return "/bcpp_household/householdsurveyreport/%s/" % self.id

    def get_url(self):
        return "/bcpp_household/householdsurveyreport/"

    def calendar_datetime(self):
        return self.survey_date

    def calendar_label(self):
        return '%s %s' % (self.__unicode__(), self.household_survey_status)

    def calendar_absolute_url(self):
        return self.household_survey.household.householdstructure.get_absolute_url()

    def group_permissions(self):
        return {'survey': ('add', 'change')}

    class Meta:
        unique_together = (
            ('household_survey', 'survey_date', 'survey_start_time'),
            )
        ordering = ['-survey_date', 'survey_start_time']
        app_label = 'bcpp_household'

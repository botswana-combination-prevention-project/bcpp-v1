from datetime import datetime
from django.db import models
from django.core.exceptions import MultipleObjectsReturned, ImproperlyConfigured
from django.conf import settings


class SurveyManager(models.Manager):

    def get_by_natural_key(self, survey_name):
        return self.get(survey_name=survey_name)

#     def current_survey(self):
#         """Returns the instance of the current survey based on today's date or None."""
#         current_survey = None
#         if super(SurveyManager, self).filter(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today()).count() == 1:
#             current_survey = super(SurveyManager, self).get(datetime_start__lte=datetime.today(), datetime_end__gte=datetime.today())
#         return current_survey

    def current_survey(self, report_datetime=None, survey_slug=None, datetime_label=None):
        """Returns a survey instance or None.

        The return value may be:
        * the current survey based on today's date and the
          settings attribute CURRENT_SURVEY;
        * a survey relative to the given report_datetime and survey_slug;
        * None if both survey_slug and settings.CURRENT are None."""
        survey = None
        report_datetime = report_datetime or datetime.today()
        survey_slug = survey_slug or settings.CURRENT_SURVEY
        datetime_label = datetime_label or 'report_datetime'
        try:
            survey = self.get(
                datetime_start__lte=report_datetime,
                datetime_end__gte=report_datetime)
            if survey_slug:
                survey = self.get(
                    datetime_start__lte=report_datetime,
                    datetime_end__gte=report_datetime,
                    survey_slug=survey_slug)
        except MultipleObjectsReturned:
            raise ImproperlyConfigured('Date {} falls within more than one Survey. Start and end dates'
                                       'may not overlap between Surveys. Check the survey configuration.'.format(
                                           report_datetime))
        except self.model.DoesNotExist:
            raise ImproperlyConfigured(
                'Expected survey \'{0}\'. {2} {1} does not fall within '
                'the start/end dates of Survey \'{0}\'.'.format(
                    survey_slug,
                    report_datetime.strftime('%Y-%m-%d'),
                    '{}{}'.format(datetime_label[0].upper(), datetime_label[1:])
                    )
                )

        return survey

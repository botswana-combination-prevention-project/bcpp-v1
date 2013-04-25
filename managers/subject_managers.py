from django.db import models
from django.db.models.query import QuerySet


class SubjectManager(models.Manager):

    def get_query_set(self):
        return QuerySet(self.model, using=self._db).filter(survey__survey_slug=self.survey_slug())


class SubjectYearOneManager(SubjectManager):

    def survey_slug(self):
        return 'bcpp-year-1'


class SubjectYearTwoManager(SubjectManager):

    def survey_slug(self):
        return 'bcpp-year-2'


class SubjectYearThreeManager(SubjectManager):

    def survey_slug(self):
        return 'bcpp-year-3'


class SubjectYearFourManager(SubjectManager):

    def survey_slug(self):
        return 'bcpp-year-4'


class SubjectYearFiveManager(SubjectManager):

    def survey_slug(self):
        return 'bcpp-year-5'

from django.db import models
from django.db.models.query import QuerySet
from bhp_visit_tracking.managers import BaseVisitTrackingManager


class SubjectVisitManager(BaseVisitTrackingManager):

    def get_query_set(self):
        return QuerySet(self.model, using=self._db).filter(subject_visit__survey__survey_slug=self.survey_slug())


class SubjectVisitYearOneManager(SubjectVisitManager):

    def survey_slug(self):
        return 'bcpp-year-1'


class SubjectVisitYearTwoManager(SubjectVisitManager):

    def survey_slug(self):
        return 'bcpp-year-2'


class SubjectVisitYearThreeManager(SubjectVisitManager):

    def survey_slug(self):
        return 'bcpp-year-3'


class SubjectVisitYearFourManager(SubjectVisitManager):

    def survey_slug(self):
        return 'bcpp-year-4'


class SubjectVisitYearFiveManager(SubjectVisitManager):

    def survey_slug(self):
        return 'bcpp-year-5'

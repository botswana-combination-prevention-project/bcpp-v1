from django.db import models
from base_visit_tracking import BaseVisitTracking
from bhp_base_model.models import BaseUuidModel


class TestSubjectVisit(BaseVisitTracking):

    def get_requires_consent(self):
        return False

    class Meta:
        app_label = 'bhp_visit_tracking'


class TestSubjectVisitTwo(BaseVisitTracking):

    def get_requires_consent(self):
        return False

    class Meta:
        app_label = 'bhp_visit_tracking'


class TestSubjectVisitThree(BaseVisitTracking):

    def get_requires_consent(self):
        return False

    class Meta:
        app_label = 'bhp_visit_tracking'


class TestScheduledModel(BaseUuidModel):

    test_subject_visit = models.OneToOneField(TestSubjectVisit)

    class Meta:
        app_label = 'bhp_visit_tracking'
    
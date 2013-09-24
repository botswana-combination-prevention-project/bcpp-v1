from django.db import models
from bhp_base_model.models import BaseUuidModel
from test_visit import TestVisit


class TestScheduledModel(BaseUuidModel):

    test_visit = models.OneToOneField(TestVisit)

    def get_subject_identifier(self):
        return self.test_visit.get_subject_identifier()

    class Meta:
        app_label = 'bhp_base_test'

from django.db import models
from bhp_base_model.models import BaseUuidModel
from test_visit import TestVisit


class TestScheduledModel(BaseUuidModel):

    test_visit = models.OneToOneField(TestVisit)

    class Meta:
        app_label = 'bhp_base_test'

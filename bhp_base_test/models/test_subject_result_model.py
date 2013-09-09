from django.db import models
from bhp_base_model.models import BaseUuidModel
from test_visit import TestVisit


class TestSubjectResultModel(BaseUuidModel):

    test_visit = models.ForeignKey(TestVisit, null=True)
    subject_identifier = models.CharField(max_length=25, db_index=True)
    report_datetime = models.DateTimeField(null=True, db_index=True)
    result = models.CharField(max_length=25)
    result_datetime = models.DateTimeField()

    def get_report_datetime(self):
        return self.result_datetime

    def get_test_code(self):
        return 'HIV'

    def get_result_datetime(self):
        return self.result_datetime

    def get_subject_identifier(self):
        return self.subject_identifier

    class Meta:
        app_label = 'bhp_base_test'

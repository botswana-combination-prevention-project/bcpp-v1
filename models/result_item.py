import logging
from django.db import models
from lab_result_item.models import BaseResultItem
from lab_clinic_reference.classes import ReferenceRangeFlag, GradeFlag
from test_code import TestCode
from result import Result


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class ResultItem(BaseResultItem):

    test_code = models.ForeignKey(TestCode, related_name='+')

    result = models.ForeignKey(Result)

    import_datetime = models.DateTimeField(null=True)

    objects = models.Manager()

    def __unicode__(self):
        return unicode(self.test_code)

    def to_result(self):
        return '<a href="/admin/lab_clinic_api/result/?q={result_identifier}">{result_identifier}</a>'.format(result_identifier=self.result.result_identifier)
    to_result.allow_tags = True

    def get_subject_identifier(self):
        return self.result.order.aliquot.receive.registered_subject.subject_identifier

    def get_grading_list(self):
        return ('grading_list', models.get_model('lab_clinic_reference', 'gradinglistitem'))

    def get_cls_reference_flag(self):
        return ReferenceRangeFlag

    def get_cls_grade_flag(self):
        return GradeFlag

    def get_reference_list(self):
        return ('reference_range_list', models.get_model('lab_clinic_reference', 'referencerangelistitem'))

    class Meta:
        app_label = "lab_clinic_api"

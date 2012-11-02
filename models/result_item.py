import logging
from django.db import models
from lab_result_item.models import BaseResultItem
from lab_clinic_reference.classes import ClinicReferenceFlag, ClinicGradeFlag
from test_code import TestCode
from result import Result


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class ResultItem(BaseResultItem):
    """Stores each result item in a result in one-to-many relation with :class:`Result`."""
    test_code = models.ForeignKey(TestCode, related_name='+')
    result = models.ForeignKey(Result)
    subject_type = models.CharField(max_length=25, null=True)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.subject_identifier = self.result.order.aliquot.receive.registered_subject.subject_identifier
        self.receive_identifier = self.result.order.aliquot.receive.receive_identifier
        self.subject_type = self.get_subject_type()
        super(ResultItem, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.test_code)

    def result_value(self):
        if self.result_item_value_as_float:
            return self.result_item_value_as_float
        else:
            return self.result_item_value

    def to_result(self):
        return '<a href="/admin/lab_clinic_api/result/?q={result_identifier}">result</a>'.format(result_identifier=self.result.result_identifier)
    to_result.allow_tags = True

    def get_subject_type(self):
        if not self.subject_type:
            return self.result.order.aliquot.receive.registered_subject.subject_type
        else:
            return self.subject_type

    def get_grading_list(self):
        return ('grading_list', models.get_model('lab_clinic_reference', 'gradinglistitem'))

    def get_cls_reference_flag(self):
        return ClinicReferenceFlag

    def get_cls_grade_flag(self):
        return ClinicGradeFlag

    def get_reference_list(self):
        #pdb.set_trace()
        return ('reference_range_list', models.get_model('lab_clinic_reference', 'referencerangelistitem'))

    class Meta:
        app_label = "lab_clinic_api"

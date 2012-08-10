import logging
from django.db import models
from lab_result_item.models import BaseResultItem
from lab_reference.classes import ReferenceFlag
from lab_grading.classes import GradeFlag
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

    objects = models.Manager()

    def __unicode__(self):
        return unicode(self.test_code)

    def get_subject_identifier(self):
        return self.result.order.aliquot.receive.registered_subject.subject_identifier

    def save(self, *args, **kwargs):

        # save the result to update the modified datetime
        #self.result.save()

        if not self.result.order.aliquot.receive.registered_subject:
            logger.warning('ResultItem expected registered subject from the receive instance. Got None')
        else:
            reference_flag = ReferenceFlag()
            reference_flag.result_item_value = self.result_item_value
            reference_flag.dob = self.result.order.aliquot.receive.registered_subject.dob
            reference_flag.gender = self.result.order.aliquot.receive.registered_subject.gender
            reference_flag.drawn_datetime = self.result.order.aliquot.receive.drawn_datetime
            reference_flag.test_code = self.test_code
            if reference_flag.flag:
                self.reference_range = '%s - %s' % (reference_flag.flag['range']['lln'], reference_flag.flag['range']['uln'])
                self.reference_flag = reference_flag.flag['flag']
            grade = GradeFlag()
            grade.result_item_value = self.result_item_value
            grade.dob = self.result.order.aliquot.receive.registered_subject.dob
            grade.gender = self.result.order.aliquot.receive.registered_subject.gender
            grade.drawn_datetime = self.result.order.aliquot.receive.drawn_datetime
            # ..todo:: TODO: if more than one test, hiv status is not correct
            grade.hiv_status = self.result.order.aliquot.receive.registered_subject.hiv_status or 'any'
            grade.test_code = self.test_code
            if grade.flag:
                self.grade_range = '%s - %s' % (grade.flag['range']['lln'], grade.flag['range']['uln'])
                self.grade_flag = grade.flag['flag']

        return super(ResultItem, self).save(*args, **kwargs)

    class Meta:
        app_label = "lab_clinic_api"

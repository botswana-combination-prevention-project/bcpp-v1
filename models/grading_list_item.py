from django.db import models
from lab_reference.models import BaseReferenceListItem
from lab_reference.utils import get_lower_range_days, get_upper_range_days
from lab_grading.models import GradingList
from lab_test_code.models import TestCode


class GradingListItem(BaseReferenceListItem):

    test_code = models.ForeignKey(TestCode)

    grading_list = models.ForeignKey(GradingList)

    grade = models.IntegerField()

    objects = models.Manager()

    def __unicode__(self):
        return "%s" % (unicode(self.test_code))

    class Meta:
        app_label = 'lab_grading'
        ordering = ['test_code', 'age_low', 'age_low_unit']
        db_table = 'lab_grading_gradinglistitem'

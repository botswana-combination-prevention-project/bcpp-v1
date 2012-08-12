from django.db import models
from bhp_common.choices import POS_NEG_ANY
from lab_reference.models import BaseReferenceListItem
from lab_reference.utils import get_lower_range_days, get_upper_range_days
from lab_clinic_api.models import TestCode
from grading_list import GradingList


class GradingListItem(BaseReferenceListItem):

    test_code = models.ForeignKey(TestCode)

    grading_list = models.ForeignKey(GradingList)

    hiv_status = models.CharField(
        max_length=10,
        choices=POS_NEG_ANY,
        default='ANY',
        )

    grade = models.IntegerField()

    """
        lower |    upper
        ------|-------------
        m*30  |    (1+m)*30)-1
        y*365 |    (1+y)*365)-1
    """

    objects = models.Manager()

    def age_low_days(self):
        return get_lower_range_days(self.age_low, self.age_low_unit)

    def age_high_days(self):
        return get_upper_range_days(self.age_high, self.age_high_unit)

    def __unicode__(self):
        return self.test_code.code

    class Meta:
        app_label = 'lab_clinic_reference'
        ordering = ['test_code', 'age_low', 'age_low_unit']

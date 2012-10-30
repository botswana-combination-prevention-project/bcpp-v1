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

    import_datetime = models.DateTimeField(null=True)

    """
        lower |    upper
        ------|-------------
        m*30  |    (1+m)*30)-1
        y*365 |    (1+y)*365)-1
    """

    objects = models.Manager()

    def describe(self, age_in_days=None):
        if not age_in_days:
            age_in_days = 'AGE'
        if self.scale == 'increasing':
            template = 'G{grade} {gender} HIV-{hiv_status} VAL{uln_quantifier}{uln} and VAL{lln_quantifier}{lln} for {age_in_days}{age_low_quantifier}{age_low_days}d and {age_in_days}{age_high_quantifier}{age_high_days}d'
        else:
            template = 'G{grade} {gender} HIV-{hiv_status} VAL{lln_quantifier}{lln} and VAL{uln_quantifier}{uln} for {age_in_days}{age_low_quantifier}{age_low_days}d and {age_in_days}{age_high_quantifier}{age_high_days}d'
        return template.format(
            grade=self.grade,
            gender=self.gender,
            hiv_status=self.hiv_status,
            lln_quantifier=self.lln_quantifier,
            uln_quantifier=self.uln_quantifier,
            lln=self.round_off(self.lln),
            uln=self.round_off(self.uln),
            age_in_days=age_in_days,
            age_low_quantifier=self.age_low_quantifier,
            age_low_days=self.age_low_days(),
            age_high_quantifier=self.age_high_quantifier,
            age_high_days=self.age_high_days())

    def round_off(self, value):
        return round(value, self.test_code.display_decimal_places or 0)

    def age_low_days(self):
        return get_lower_range_days(self.age_low, self.age_low_unit)

    def age_high_days(self):
        return get_upper_range_days(self.age_high, self.age_high_unit)

    def __unicode__(self):
        return '{0} {1}'.format(self.test_code.code, self.grade)

    class Meta:
        app_label = 'lab_clinic_reference'
        ordering = ['test_code', 'age_low', 'age_low_unit']

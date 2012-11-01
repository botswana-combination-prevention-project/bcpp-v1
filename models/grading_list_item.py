from django.db import models
from audit_trail.audit import AuditTrail
from lab_reference.models import BaseReferenceListItem
from lab_clinic_api.models import TestCode
from grading_list import GradingList


class GradingListItem(BaseReferenceListItem):

    test_code = models.ForeignKey(TestCode)

    grading_list = models.ForeignKey(GradingList)

    grade = models.IntegerField()

    import_datetime = models.DateTimeField(null=True)

    history = AuditTrail()

    objects = models.Manager()

    def describe(self, age_in_days=None):
        if not age_in_days:
            age_in_days = 'AGE'
        if self.scale == 'increasing':
            template = ('G{grade} {gender} HIV-{hiv_status} VAL{value_high_quantifier}{value_high} and '
                        'VAL{value_low_quantifier}{value_low} for {age_in_days}{age_low_quantifier}{age_low_days}d '
                        'and {age_in_days}{age_high_quantifier}{age_high_days}d')
        else:
            template = ('G{grade} {gender} HIV-{hiv_status} VAL{value_low_quantifier}{value_low} and '
                        'VAL{value_high_quantifier}{value_high} for {age_in_days}{age_low_quantifier}{age_low_days}d '
                        'and {age_in_days}{age_high_quantifier}{age_high_days}d')
        return template.format(
            grade=self.grade,
            gender=self.gender,
            hiv_status=self.hiv_status,
            value_low_quantifier=self.value_low_quantifier,
            value_high_quantifier=self.value_high_quantifier,
            value_low=self.round_off(self.value_low),
            value_high=self.round_off(self.value_high),
            age_in_days=age_in_days,
            age_low_quantifier=self.age_low_quantifier,
            age_low_days=self.age_low_days(),
            age_high_quantifier=self.age_high_quantifier,
            age_high_days=self.age_high_days())

    def __unicode__(self):
        return '{0} {1}'.format(self.test_code.code, self.grade)

    class Meta:
        app_label = 'lab_clinic_reference'
        ordering = ['test_code', 'age_low', 'age_low_unit']

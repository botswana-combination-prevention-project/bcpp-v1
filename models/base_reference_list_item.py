from django.db import models
from bhp_base_model.classes import BaseModel
from bhp_common.choices import POS_NEG_ANY
from lab_reference.choices import GENDER_OF_REFERENCE
from lab_reference.utils import get_lower_range_days, get_upper_range_days


class BaseReferenceListItem(BaseModel):

    code = models.CharField(max_length=25, null=True, blank=True)

    scale = models.CharField(
        max_length=25,
        choices=(('increasing', 'increasing'),
                 ('decreasing', 'decreasing')),
        default='increasing')

    gender = models.CharField(
        verbose_name="Gender",
        choices=GENDER_OF_REFERENCE,
        max_length=10,
        )

    hiv_status = models.CharField(
        max_length=10,
        choices=POS_NEG_ANY,
        default='ANY',
        )

    value_low = models.DecimalField(
        verbose_name='lower',
        null=True,
        max_digits=12,
        decimal_places=4,
        blank=True)

    value_low_quantifier = models.CharField(max_length=10, default='>=')

    value_high = models.DecimalField(
        verbose_name='upper',
        null=True,
        max_digits=12,
        decimal_places=4,
        blank=True)

    value_high_quantifier = models.CharField(max_length=10, default='<=')

    age_low = models.IntegerField(
        null=True,
        blank=True)

    age_low_unit = models.CharField(
        max_length=10,
        blank=True
        )

    age_low_quantifier = models.CharField(max_length=10, blank=True)

    age_high = models.IntegerField(null=True, blank=True)

    age_high_unit = models.CharField(max_length=10, blank=True)

    age_high_quantifier = models.CharField(max_length=10, blank=True)

    panic_value_low = models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)

    panic_value_high = models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)

    active = models.BooleanField(default=True, help_text="if flagged as inactive, will not be used for evaluation.")

    dummy = models.BooleanField(default=False, help_text="True if no values for this grade/range, e.g. infant Bilirubin.")

    comment = models.CharField(
        verbose_name="Comment",
        max_length=250,
        blank=True,
        )

    import_datetime = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    def round_off(self, value):
        return round(value, self.test_code.display_decimal_places or 0)

    def age_low_days(self):
        return get_lower_range_days(self.age_low, self.age_low_unit)

    def age_high_days(self):
        return get_upper_range_days(self.age_high, self.age_high_unit)

    class Meta:
        abstract = True

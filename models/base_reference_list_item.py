from django.db import models
from bhp_base_model.classes import BaseModel
from lab_reference.choices import GENDER_OF_REFERENCE


class BaseReferenceListItem(BaseModel):

    code = models.CharField(max_length=25, null=True)

    scale = models.CharField(
        max_length=25,
        choices=(('increasing', 'increasing'), ('decreasing', 'decreasing')),
        default='increasing')

    gender = models.CharField(
        verbose_name="Gender",
        choices=GENDER_OF_REFERENCE,
        max_length=10,
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

    comment = models.CharField(
        verbose_name="Comment",
        max_length=250,
        blank=True,
        )

    objects = models.Manager()

    class Meta:
        abstract = True

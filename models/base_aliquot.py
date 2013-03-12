import datetime
from django.db import models
from lab_base_model.models import BaseLabUuidModel
from lab_aliquot.choices import ALIQUOT_STATUS, SPECIMEN_MEASURE_UNITS, SPECIMEN_MEDIUM


class BaseAliquot (BaseLabUuidModel):

    aliquot_identifier = models.CharField(
        verbose_name='Aliquot Identifier',
        max_length=25,
        unique=True,
        help_text="Aliquot identifier",
        editable=False)
    aliquot_datetime = models.DateTimeField(
        verbose_name="Date and time aliquot created",
        default=datetime.datetime.today())
    count = models.IntegerField(
        editable=False,
        null=True)
    medium = models.CharField(
        verbose_name='Medium',
        max_length=25,
        choices=SPECIMEN_MEDIUM,
        default='TUBE')
    original_measure = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default='5.00')
    current_measure = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default='5.00')
    measure_units = models.CharField(
        max_length=25,
        choices=SPECIMEN_MEASURE_UNITS,
        default='mL')
    status = models.CharField(
        max_length=25,
        choices=ALIQUOT_STATUS,
        default='available')
    comment = models.CharField(
        max_length=50,
        null=True,
        blank=True)
    import_datetime = models.DateTimeField(null=True)

    def __unicode__(self):
        return '%s' % (self.aliquot_identifier)

    class Meta:
        abstract = True

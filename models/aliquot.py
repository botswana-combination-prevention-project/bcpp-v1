from django.db import models
from lab_aliquot.models import BaseAliquot
from receive import Receive
from aliquot_type import AliquotType
from aliquot_condition import AliquotCondition


class Aliquot(BaseAliquot):
    """Stores aliquot information and is the central model in the RAORR relational model."""
    aliquot_type = models.ForeignKey(AliquotType,
        verbose_name="Aliquot Type",
        null=True)
    aliquot_condition = models.ForeignKey(AliquotCondition,
        verbose_name="Aliquot Condition",
        null=True)
    receive = models.ForeignKey(Receive)
    subject_identifier = models.CharField(
        max_length=25,
        null=True,
        editable=False,
        db_index=True,
        help_text="non-user helper field to simplify search and filtering")
    objects = models.Manager()

    def __unicode__(self):
        return '%s' % (self.aliquot_identifier)

    def save(self, *args, **kwargs):
        self.subject_identifier = self.receive.registered_subject.subject_identifier
        super(Aliquot, self).save(*args, **kwargs)

    class Meta:
        app_label = 'lab_clinic_api'

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
    receive_identifier = models.CharField(
        max_length=25, editable=False, null=True, db_index=True,
        help_text="non-user helper field to simplify search and filter")
    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.subject_identifier = self.receive.registered_subject.subject_identifier
        self.receive_identifier = self.receive.receive_identifier
        if AliquotCondition.objects.filter(short_name='10'):
            aliquot_condition_ok = AliquotCondition.objects.get(short_name='10')
        else:
            raise TypeError('AliquotCondition must have at least one entry that has short_name=10 for condition is OK. Got None')
        if self.aliquot_condition:
            # TODO: fix this...
            # this IF is here because i cannot figure out how this aliquot condition crept in
            # somewhere on the import id=10 instead of short_name=10??
            if self.aliquot_condition.short_name == '4294967287':
                self.aliquot_condition = aliquot_condition_ok
        super(Aliquot, self).save(*args, **kwargs)

    def drawn(self):
        return self.receive.drawn_datetime

    def to_receive(self):
        return '<a href="/admin/lab_clinic_api/receive/?q={receive_identifier}">{receive_identifier}</a>'.format(receive_identifier=self.receive.receive_identifier)
    to_receive.allow_tags = True

    def __unicode__(self):
        return '%s' % (self.aliquot_identifier)

    class Meta:
        app_label = 'lab_clinic_api'

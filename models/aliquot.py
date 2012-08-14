from django.db import models
from lab_aliquot.models import BaseAliquot
from receive import Receive
from aliquot_type import AliquotType
from aliquot_condition import AliquotCondition


class Aliquot(BaseAliquot):

    aliquot_type = models.ForeignKey(AliquotType,
        verbose_name="Aliquot Type",
        null=True,
        )

    aliquot_condition = models.ForeignKey(AliquotCondition,
        verbose_name="Aliquot Condition",
        null=True,
        )

    receive = models.ForeignKey(Receive)

    import_datetime = models.DateTimeField(null=True)

    objects = models.Manager()

    def __unicode__(self):
        return '%s' % (self.aliquot_identifier)

    class Meta:
        app_label = 'lab_clinic_api'
        #ordering =['result_identifier']

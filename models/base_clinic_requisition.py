from django.db import models
from django.core.serializers.base import SerializationError
from bhp_visit_tracking.models import BaseVisitTracking
from lab_requisition.models import BaseRequisition


class BaseClinicRequisition (BaseRequisition):

    dmis_identifier = models.CharField(max_length=25, null=True, editable=False)

    def get_visit(self):
        for field in self._meta.fields:
            try:
                if issubclass(field.rel.to, BaseVisitTracking):
                    return field.rel.to.objects.get(pk=getattr(self, field.attname))
            except:
                pass
        raise TypeError('{0} is unable to determine the visit model'.format(self))
        return None

    def get_subject_identifier(self):
        return self.get_visit().appointment.registered_subject.subject_identifier

    def natural_key(self):
        raise SerializationError('Requisition subclass must override method \'natural key\'.')

    class Meta:
        abstract = True

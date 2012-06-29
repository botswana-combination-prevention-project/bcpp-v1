from bhp_visit_tracking.models import BaseVisitTracking
from lab_requisition.models import BaseRequisition
from lab_requisition.classes import ClinicRequisitionLabel


class BaseClinicRequisition (BaseRequisition):
    
    def get_label(self, **kwargs):
        
        label = ClinicRequisitionLabel(
                    client_ip = kwargs.get('remote_addr'),
                    cups_server_ip = kwargs.get('cups_server_ip'),
                    item_count = kwargs.get('item_count'), 
                    requisition = self)
        return label
    
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


    class Meta:
        abstract = True

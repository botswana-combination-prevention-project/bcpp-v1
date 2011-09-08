from lab_barcode.models import ZplTemplate
from requisition_label import RequisitionLabel


class ClinicRequisitionLabel(RequisitionLabel):

    def __init__(self, **kwargs):

        if not ZplTemplate.objects.filter(name='clinic specimen label'):
            raise ValueError, 'Requisition requires a zpl_template named \'clinic specimen label\'. Please define a template named \'clinic specimen label\' in model ZplTemplate.'
        else:        
            kwargs['template'] = ZplTemplate.objects.get(name='clinic specimen label')
            kwargs['reprint'] = 'reprint'

        super(ClinicRequisitionLabel, self).__init__(**kwargs)

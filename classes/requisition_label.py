from bhp_variables.models import StudySpecific
from bhp_registration.models import RegisteredSubject
from lab_barcode.classes import Label

class RequisitionLabel(Label):

    def __init__(self, **kwargs):
        
        requisition = kwargs.get('requisition')
        template = kwargs.get('template')        
        item_count = kwargs.get('item_count', 1)
        try:
            study_specific = StudySpecific.objects.all()[0]
        except:
            raise AttributeError, 'Cannot determine protocol_number. Please populate bhp_variables.study_specific.'    
        
        subject_identifier = requisition.get_subject_identifier()
        
        registered_subject = RegisteredSubject.objects.get(subject_identifier = subject_identifier)
        
        super(RequisitionLabel, self).__init__(
            template = template,
            requisition_identifier = requisition.requisition_identifier,
            protocol = study_specific.protocol_number,
            site = requisition.site.site_code,
            panel= requisition.panel.name[0:21],
            drawn_datetime = requisition.drawn_datetime,
            subject_identifier = subject_identifier,
            gender = registered_subject.gender,
            dob = registered_subject.dob,
            initials = registered_subject.initials,
            may_store_samples = registered_subject.may_store_samples,
            aliquot_type = requisition.aliquot_type.alpha_code.upper(),
            item_count = item_count,
            item_count_total = requisition.item_count_total,
            )
    
               

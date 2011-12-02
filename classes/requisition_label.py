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
        
        if registered_subject.may_store_samples.lower() == 'Yes':
            may_store_samples = 'Y'
        elif registered_subject.may_store_samples.lower() == 'No':            
            may_store_samples = 'N'        
        else:
            may_store_samples = '?'                    

        kwargs['template'] = template
        kwargs['requisition_identifier'] = requisition.requisition_identifier
        kwargs['specimen_identifier'] = requisition.specimen_identifier
        if 'hiv_status_code' in dir(requisition):
            kwargs['hiv_status_code'] = str(requisition.hiv_status_code())
        if 'art_status_code' in dir(requisition):
            kwargs['art_status_code'] = str(requisition.art_status_code())
        kwargs['protocol'] = study_specific.protocol_number
        kwargs['site'] = requisition.site.site_code
        kwargs['panel']= requisition.panel.name[0:21]
        kwargs['drawn_datetime'] = requisition.drawn_datetime
        kwargs['subject_identifier'] = subject_identifier
        kwargs['gender'] = registered_subject.gender
        kwargs['dob'] = registered_subject.dob
        kwargs['initials'] = registered_subject.initials
        kwargs['may_store_samples'] = may_store_samples
        kwargs['aliquot_type'] = requisition.aliquot_type.alpha_code.upper()
        kwargs['item_count'] = item_count
        kwargs['item_count_total'] = requisition.item_count_total
        
        super(RequisitionLabel, self).__init__(**kwargs)
    
               

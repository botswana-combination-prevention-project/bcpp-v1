from bhp_registration.models import RegisteredSubject
from lab_clinic_api.models import Lab
from lab_clinic_api.forms import ReviewForm


class LabContextDescriptor(object):

    def __init__(self):
        self.value = {}

    def __get__(self, instance, owner):
        if instance.receive_identifier:
            self.__set__(instance)
        return self.value

    def __set__(self, instance):
        self.value = {
            'last_updated': instance.lab.modified,
            'review_form': ReviewForm(),
            'result': [],
            'protocol_identifier': instance.lab.protocol_identifier,
            'subject_identifier': instance.lab.subject_identifier,
            'dob': instance.registered_subject.dob,
            'is_dob_estimated': instance.registered_subject.is_dob_estimated,
            'gender': instance.registered_subject.gender,
            'initials': instance.registered_subject.initials,
            'site_identifier':instance.registered_subject.study_site.site_name,
            'clinicians_initials': instance.lab.clinician_initials,        
            'drawn_datetime': instance.lab.drawn_datetime,
            'panel_name': instance.lab.panel,
            'receive_identifier': instance.lab.receive_identifier,        
            'receive_datetime': instance.lab.receive_datetime,        
            'aliquot_identifier': instance.lab.aliquot_identifier,
            'order_identifier': instance.lab.order_identifier,        
            'order_datetime': instance.lab.order_datetime,
            'condition': instance.lab.condition,                
            'result_items': [],
            'action':"view",        
            'section_name': instance.section_name,
            'search_name': instance.search_name,        
            'result_include_file': "detail.html",
            'receiving_include_file':"receiving.html",
            'orders_include_file': "orders.html",
            'result_items_include_file': "result_items.html",
            'top_result_include_file': "result_include.html",
        }


class LabContext(object):

    context = LabContextDescriptor()
    
    def __init__(self, **kwargs):
        self.section_name = kwargs.get('section_name')
        self.search_name = kwargs.get('search_name')        
        self.receive_identifier = kwargs.get('receive_identifier')
        if self.receive_identifier:
            self.lab = Lab.objects.get(receive_identifier__exact=self.receive_identifier)
            self.registered_subject = RegisteredSubject.objects.get(subject_identifier=self.lab.subject_identifier)        


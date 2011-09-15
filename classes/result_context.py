from bhp_registration.models import RegisteredSubject
from lab_clinic_api.models import Result, ResultItem
from lab_clinic_api.forms import ReviewForm


class ContextDescriptor(object):

    def __init__(self):
        self.value = {}

    def __get__(self, instance, owner):
        if instance.result_identifier:
            self.__set__(instance)
        return self.value

    def __set__(self, instance):
        self.value = {
            'last_updated': instance.result.modified,
            'review_form': ReviewForm(),
            'result': instance.result,
            'protocol_identifier': instance.result.lab.protocol_identifier,
            'subject_identifier': instance.result.lab.subject_identifier,
            'dob': instance.registered_subject.dob,
            'is_dob_estimated': instance.registered_subject.is_dob_estimated,
            'gender': instance.registered_subject.gender,
            'initials': instance.registered_subject.initials,
            'site_identifier':instance.registered_subject.study_site.site_name,
            'clinicians_initials': instance.result.lab.clinician_initials,        
            'drawn_datetime': instance.result.lab.drawn_datetime,
            'panel_name': instance.result.lab.panel,
            'receive_identifier': instance.result.lab.receive_identifier,        
            'receive_datetime': instance.result.lab.receive_datetime,        
            'aliquot_identifier': instance.result.lab.aliquot_identifier,
            'order_identifier': instance.result.lab.order_identifier,        
            'order_datetime': instance.result.lab.order_datetime,
            'condition': instance.result.lab.condition,                
            'result_items': instance.result_items,
            'action':"view",        
            'section_name': instance.section_name,
            'search_name': instance.search_name,        
            'result_include_file': "detail.html",
            'receiving_include_file':"receiving.html",
            'orders_include_file': "orders.html",
            'result_items_include_file': "result_items.html",
            'top_result_include_file': "result_include.html",
        }


class ResultContext(object):

    context = ContextDescriptor()
    
    def __init__(self, **kwargs):
        self.section_name = kwargs.get('section_name')
        self.search_name = kwargs.get('search_name')        
        self.result_identifier = kwargs.get('result_identifier')
        if self.result_identifier:
            self.result = Result.objects.get(lab__result_identifier__exact=self.result_identifier)
            self.result_items = ResultItem.objects.filter(result=self.result)
            self.registered_subject = RegisteredSubject.objects.get(subject_identifier=self.result.lab.subject_identifier)        


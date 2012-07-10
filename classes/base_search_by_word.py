from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from bhp_registration.models import RegisteredSubject
from bhp_consent.classes import BaseConsent
from bhp_crypto.classes import BaseEncryptedField
#from bhp_crypto.classes import CryptoQ as Q
from bhp_search.forms import SearchForm
from base_search import BaseSearch



class BaseSearchByWord(BaseSearch):

    def __init__(self, request, **kwargs):
        
        super(BaseSearchByWord, self).__init__(request, 'word', **kwargs )
        defaults = {'search_helptext':'Search by search term.'}
        self.search_form = SearchForm 
        self.context.update(**defaults) 
    
    def search(self, request, **kwargs):
        """get word or search term queryset object based on a name or 'queryset_label'"""        
        #self.update_context(search_term=search_term)                  
        for model_name, model in self.search_model.iteritems():
            if not isinstance(model(), RegisteredSubject):
                if not 'registered_subject' in dir(model()) and not isinstance(model(), BaseConsent):
                    raise ImproperlyConfigured('Search models must have a foreign key to model RegisteredSubject or be a subclass of BaseConsent. Got model {0}.'.format(model_name) )
        if not self.context.get('search_term'):
            raise TypeError('Search method should only be called if the \'search_term\' is known. Got None')
        #may pass a search term that is k1=v1+k2=v2+k3=v3 ...
        #        terms = self.context.get('search_term').split('+')
        #        search_terms={}
        #        search_terms['word']=[]
        #        search_terms['number']=[]
        #        search_terms['gender']=[]
        #        search_terms['date']=[]
        #        search_terms['yyyy_mm']=[]
        #        search_terms['yyyy']=[]
        #        search_terms['uuid']=[]                                                                            
        #        for t in terms:
        #            #if k/v pairs, categorize
        #            if self.pattern.get('word').search(t):
        #                search_terms['word'].append(t)
        #            elif self.pattern.get('number').search(t):
        #                search_terms['number'].append(t)
        #            elif self.pattern.get('gender').search(t):
        #                search_terms['gender'].append(t)
        #            elif self.pattern.get('date').search(t):
        #                search_terms['date'].append(t)
        #            elif self.pattern.get('yyyy_mm').search(t):
        #                search_terms['yyyy_mm'].append(t)
        #            elif self.pattern.get('yyyy').search(t):
        #                search_terms['yyyy'].append(t)
        #            elif self.pattern.get('uuid').search(t):
        #                search_terms['uuid'].append(t)            
        #            else:
        #                #this is just a search term, not key/value pairs
        #                search_terms['word'].append(t)
        if not self.context.get('dbname', None):
            self.update_context(dbname='default')            
 
        if self.pattern.get('word').search(self.context.get('search_term')):
            field_contains = '%s__icontains' % (self.context.get('search_term').split('=')[0])    
            this_value = self.context.get('search_term').split('=')[1]
            self.update_context(search_result=self.search_model.get(self.search_model_name).objects.using(self.context.get('dbname')).filter( **{ field_contains : this_value } ).order_by('-created'))                
        elif self.pattern.get('number').search(self.context.get('search_term')):
            field_contains = '%s' % (self.context.get('search_term').split('=')[0])    
            this_value = self.context.get('search_term').split('=')[1]
            self.update_context(search_result=self.search_model.get(self.search_model_name).objects.using(self.context.get('dbname')).filter( **{ field_contains : this_value } ).order_by('-created'))                
        else:
            model = self.search_model.get(self.search_model_name)
            search_term = {}
            if 'registered_subject' in dir(model()):
                # model has a key to registered subject
                search_term=self.hash_for_encrypted_fields(self.context.get('search_term'), RegisteredSubject()) 
                self.update_context(order_by='registered_subject__subject_identifier')
                # prepare the qset, note that 
                qset = (
                    Q(registered_subject__subject_identifier__icontains=self.context.get('search_term')) |
                    Q(registered_subject__first_name__exact=search_term.get('first_name')) |
                    Q(registered_subject__initials__icontains=search_term.get('initials')) |
                    Q(registered_subject__sid__icontains=search_term.get('sid'))|      
                    Q(registered_subject__last_name__exact=search_term.get('last_name')) |   
                    Q(registered_subject__identity__exact=search_term.get('identity')) |                                              
                    Q(user_created__icontains=self.context.get('search_term')) |
                    Q(user_modified__icontains=self.context.get('search_term'))
                    )
            elif isinstance(model(), BaseConsent):
                # model is a subclass of BaseConsent
                search_term=self.hash_for_encrypted_fields(self.context.get('search_term'), model) 
                self.update_context(order_by='subject_identifier')
                qset = (
                    Q(subject_identifier__icontains=self.context.get('search_term')) |
                    Q(first_name__exact=search_term.get('first_name')) |
                    Q(last_name__exact=search_term.get('last_name')) |
                    Q(identity__exact=search_term.get('identity')) |
                    Q(initials__contains=search_term.get('initials')) |
                    Q(user_created__icontains=self.context.get('search_term')) |
                    Q(user_modified__icontains=self.context.get('search_term'))
                    )
            else:
                raise ImproperlyConfigured('Search models must have a foreign key to model RegisteredSubject or be a subclass of BaseConsent. Got model {0}.'.format(model_name) )
        search_result=model.objects.filter(qset).order_by(self.context.get('order_by'))
        self.update_context(count=0)
        if search_result:
            self.paginate(request.GET.get('page', '1'))    
            self.update_context(search_result=search_result)
            self.update_context(count=search_result.count())
            
    def hash_for_encrypted_fields(self, search_term, model_instance):
        """ Using the model's field objects and the search term, create a dictionary of {field_name, search term}
            where search term is hashed if this is an encrypted field """
        terms={}
        for field in model_instance._meta.fields:
            if isinstance(field, BaseEncryptedField):
                # change the search term to a hash using the hasher on the field
                terms[field.attname]=field.crypter.get_stored_hash(search_term)
            else:
                # use the original search term
                terms[field.attname]=search_term
        return terms
        


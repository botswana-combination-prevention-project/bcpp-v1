from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from bhp_registration.models import RegisteredSubject
from bhp_consent.classes import BaseConsent
from bhp_crypto.classes import BaseEncryptedField
from bhp_search.forms import SearchForm
from base_search import BaseSearch


class BaseSearchByWord(BaseSearch):

    search_type = 'word'

    def __init__(self, **kwargs):

        super(BaseSearchByWord, self).__init__(**kwargs)
        defaults = {'search_helptext': 'Search by search term.'}
        self.search_form = SearchForm
        self.context.update(**defaults)

    def prepare_form(self, request, **kwargs):
        super(BaseSearchByWord, self).prepare_form(request, **kwargs)
        if self.ready:
            self.update_context(search_result_title='Results for \'{0}\''.format(','.join([v for v in self.context.get('form').cleaned_data.itervalues()])))

    def search(self, request, **kwargs):
        """get word or search term queryset object based on a name or 'queryset_label'"""
        for model_name, model in self.search_model.iteritems():
            if not isinstance(model(), RegisteredSubject):
                if not 'registered_subject' in dir(model()) and not isinstance(model(), BaseConsent):
                    raise ImproperlyConfigured('Search models must have a foreign key to model RegisteredSubject or be a subclass of BaseConsent. Got model {0}.'.format(model_name))
        if not self.context.get('dbname', None):
            self.update_context(dbname='default')
        # expect a single k,v pair so that we have just one search term
        if len(self.context.get('form').fields) != 1:
            raise TypeError("Search-by-word form {0} should have a single field only. Got {1}".format(self.context.get('form').__class__, len(self.context.get('form').fields)))
        for field_name in self.context.get('form').fields.iterkeys():
            search_term = self.context.get('form').cleaned_data.get(field_name)
        if not search_term:
            raise TypeError('Search method should only be called if the \'search_term\' is known. Got None')
        model = self.search_model.get(self.search_model_name)
        search_term_or_hash = {}
        if 'registered_subject' in dir(model()):
            # model has a key to registered subject
            search_term_or_hash = self.hash_for_encrypted_fields(search_term, RegisteredSubject())
            self.update_context(order_by='registered_subject__subject_identifier')
            qset = (
                Q(registered_subject__subject_identifier__icontains=search_term_or_hash.get('subject_identifier')) |
                Q(registered_subject__first_name__exact=search_term_or_hash.get('first_name')) |
                Q(registered_subject__initials__icontains=search_term_or_hash.get('initials')) |
                Q(registered_subject__sid__icontains=search_term_or_hash.get('sid')) |
                Q(registered_subject__last_name__exact=search_term_or_hash.get('last_name')) |
                Q(registered_subject__identity__exact=search_term_or_hash.get('identity')) |
                Q(user_created__icontains=search_term_or_hash.get('user_created')) |
                Q(user_modified__icontains=search_term_or_hash.get('user_modified'))
                )
        elif isinstance(model(), BaseConsent):
            # model is a subclass of BaseConsent
            search_term_or_hash = self.hash_for_encrypted_fields(search_term, model)
            self.update_context(order_by='subject_identifier')
            qset = (
                Q(subject_identifier__icontains=search_term_or_hash.get('subject_identifier')) |
                Q(first_name__exact=search_term_or_hash.get('first_name')) |
                Q(last_name__exact=search_term_or_hash.get('last_name')) |
                Q(identity__exact=search_term_or_hash.get('identity')) |
                Q(initials__contains=search_term_or_hash.get('initials')) |
                Q(user_created__icontains=search_term_or_hash.get('user_created')) |
                Q(user_modified__icontains=search_term_or_hash.get('user_modified'))
                )
        else:
            raise ImproperlyConfigured('Search models must have a foreign key to model RegisteredSubject or be a subclass of BaseConsent. Got model {0}.'.format(model_name))
        search_result = model.objects.filter(qset).order_by(self.context.get('order_by'))
        kwargs.update({'search_result': search_result})
        super(BaseSearchByWord, self).search(request, **kwargs)

    def hash_for_encrypted_fields(self, search_term, model_instance):
        """ Using the model's field objects and the search term, create a dictionary of {field_name, search term}
            where search term is hashed if this is an encrypted field """
        terms = {}
        for field in model_instance._meta.fields:
            if isinstance(field, BaseEncryptedField):
                # change the search term to a hash using the hasher on the field
                terms[field.attname] = field.crypter.get_stored_hash(search_term)
            else:
                # use the original search term
                terms[field.attname] = search_term
        return terms



from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models import Q
from bhp_crypto.fields import BaseEncryptedField
from bhp_registration.models import RegisteredSubject
from bhp_consent.models import BaseConsent
from bhp_search.forms import SearchForm
from bhp_search.exceptions import SearchError
from base_search import BaseSearch


class BaseSearchByWord(BaseSearch):

    search_type = 'word'

    def __init__(self):
        super(BaseSearchByWord, self).__init__()
        self.search_helptext = 'Search by search term.'
        self.search_result_order_by = '-modified'
        defaults = {'search_helptext': 'Search by search term.'}
        self.search_form = SearchForm
        self.context.update(**defaults)

    def get_search_result(self, request):
        """Returns a queryset using the search term as a filter.

        The model to query is selected using the search_name.

        Arguments:
            search_name --

        """
        model = self.get_search_model_cls()
#         if not isinstance(model(), RegisteredSubject):
#             if not 'registered_subject' in dir(model()) and not isinstance(model(), BaseConsent):
#                 raise ImproperlyConfigured('Search models must have a foreign key to '
#                                                'model RegisteredSubject or be a subclass of '
#                                                'BaseConsent. Got model {0}.'.format(model._meta.object_name.lower()))
        if not self.context.get('dbname', None):
            self.update_context(dbname='default')
        # expect a single k,v pair so that we have just one search term
        if len(self.context.get('form').fields) != 1:
            raise TypeError('Search-by-word form {0} should have a single field only. '
                            'Got {1}'.format(self.context.get('form').__class__,
                                             len(self.context.get('form').fields)))
        for field_name in self.context.get('form').fields.iterkeys():
            search_term = self.context.get('form').cleaned_data.get(field_name)
        if not search_term:
            raise TypeError('Search method should only be called if the \'search_term\' is known. Got None')
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
        elif issubclass(model, BaseConsent):
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
            qset = Q()
            search_term_or_hash = self.hash_for_encrypted_fields(search_term, model)
            for field in model._meta.fields:
                if isinstance(field, BaseEncryptedField):
                    qset.add(Q(**{'{0}__exact'.format(field.name): search_term_or_hash.get(field.name)}), Q.OR)
                elif isinstance(field, (models.CharField, models.TextField)):
                    qset.add(Q(**{'{0}__icontains'.format(field.name): search_term_or_hash.get(field.name)}), Q.OR)
                elif isinstance(field, (models.IntegerField, models.FloatField, models.DecimalField)):
                    try:
                        x = int(search_term)
                        qset.add(Q(**{'{0}__exact'.format(field.name): search_term_or_hash.get(field.name)}), Q.OR)
                    except:
                        pass
                elif isinstance(field, (models.DateTimeField, models.DateField)):
                    pass
                else:
                    raise SearchError('model contains a field type not handled. Got {0} from model {1}.'.format(field, model))
            self.update_context(order_by=self.order_by)
#             raise ImproperlyConfigured('Search models must have a foreign key to model '
#                                        'RegisteredSubject or be a subclass of BaseConsent. '
#                                        'Got model {0}.'.format(model._meta.object_name.lower()))
        search_result = model.objects.filter(qset).order_by(self.context.get('order_by'))
        return search_result

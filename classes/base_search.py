import re
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
from django import forms
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from bhp_crypto.fields import BaseEncryptedField
from defaults import defaults
from patterns import patterns


class BaseSearch(object):

    """ Base search class. """

    APP_LABEL = 0
    MODEL_NAME = 1
    SECTION_NAME = 2

    def __init__(self):
        """
        Keyword Arguments:
            search_result_template --
            section_name --
        """
        self.form_is_valid = False
        self.registration_model = {}
        self.search_form = None
        self.search_label = None
        self.search_model_name = None
        self._section_name_list = None
        self.section_name = None
        self.search_model = {}
        self._context = {}
        self.pattern = patterns

    @property
    def context(self):
        return self._context

    def update_context(self, **kwargs):
        for k, v in kwargs.iteritems():
            self._context[k] = v

    def validate_section_name(self, section_name):
        validated = False
        if not section_name:
            raise AttributeError('section_name cannot be None')
        for v in self._get_search_models_prep().itervalues():
            if v[self.SECTION_NAME] == section_name:
                validated = True
        return validated

    def get_search_models_for_section(self, section_name):
        """Finds the search model tuples for the given section and returns a list of the search model classes."""
        search_models = []
        if not section_name:
            raise AttributeError('section_name cannot be None')
        for v in self._get_search_models_prep().itervalues():
            if v[self.SECTION_NAME] == section_name:
                search_models.append(get_model(v[self.APP_LABEL], v[self.MODEL_NAME]))
        if not search_models:
            raise TypeError('No search models found for section name {0}'.format(section_name))
        return search_models

    def prepare(self, request, **kwargs):
        self._prepare_context(request, **kwargs)
        self._prepare_form(request)

    def _prepare_context(self, request, **kwargs):

        """ Prepares the context including passing the GET/POSt to the form using
        the request object and keyword arguments coming from the url.

        Keyword Arguments:
        section_name -- section navigated from when going to search. Usually something
                        like mother, infant, subject. Specified in the template.
                        (default: None)
        search_name -- name of model to search on. e.g maternalconsent, infantbirth, ... (default: None)
        search_by -- word, date or week. Refers to the subclass initiating the search
                     (default: None)
        """
        self.update_context(**defaults)
        self.update_context(**kwargs)
        self.context.update({'search_result_template': '{0}_include.html'.format(self.context.get('search_name'))})
        self.context.update({'report_title': 'Search {0} by {1}'.format(self.context.get('search_name'), self.search_label)})
        self.context.update({'extend': 'base_search_by_{0}.html'.format(self.search_label)})
        self.context.update({'search_by_name': self.search_label})
        self.context.update({'section_name': self.section_name})
        if request.method == 'POST':
            self.update_context(magic_url=request.POST.urlencode())
        elif request.method == 'GET':
            if request.POST.urlencode():
                self.update_context(magic_url=request.GET.urlencode())

    def _prepare_form(self, request):
        """ Updates the context with the search form and updates
        the search form with POST or GET. """
        # setup the search form
        self.form_is_valid = False
        if not issubclass(self.search_form, forms.Form):
            raise TypeError('Expected subclass of forms.Form for attribute \'search_form\'. Got {0}'.format(self.search_form))
        if ((request.method == 'GET' and not request.GET == {}) or (request.method == 'POST' and not request.POST == {})):
            if request.method == 'POST':
                self.context.update(form=self.search_form(request.POST))
            elif request.method == 'GET':
                self.context.update(form=self.search_form(request.GET))
            else:
                raise TypeError('Request method unknown. Expected POST or GET. See BaseSearch')
            if self.context.get('form').is_valid():
                if request.method == 'POST':
                    self.update_context(magic_url=request.POST.urlencode())
                elif request.method == 'GET':
                    self.update_context(magic_url=request.GET.urlencode())
                self.form_is_valid = True
        else:
            self.update_context(form=self.search_form())
        if self.form_is_valid:
            self.update_context(search_result_title='Results for \'{0}\''.format(','.join([v for v in self.context.get('form').cleaned_data.itervalues()])))

    def get_most_recent_model(self):
        return None

    def get_most_recent(self, model_name=None, page=1, limit=None):
        """Returns a queryset of the top most recent instances of the search model.

        Not technically a search function but it does use the other attributes like search_name...
        This is usually called from your section_index view."""
        if not limit:
            if 'MOST_RECENT_LIMIT' in dir(settings):
                limit = settings.MOST_RECENT_LIMIT
            else:
                limit = 10
        if model_name and limit > 0:
            model = self._get_search_model(model_name)
            search_result = model.objects.all().order_by('-created')[0:limit]
            return self._paginate(search_result, page)
        return None

    def search(self, request):
        """
        Updates the context with the search results and has the queryset paginated.

        Keyword Arguments:
        search_result --
        """
        search_result = self._get_search_result(request, self.search_name)
        page = request.GET.get('page', '1')
        if search_result:
            count = search_result.count()
            search_result = self._paginate(search_result, page)
            # Make sure page request is an int. If not, deliver first page.
            self.update_context(page=page)
            # If page request (9999) is out of range, deliver last page of results.
            self.update_context(search_result=search_result)
            self.update_context(count=count)
            # remove page= from GET url
            self.context.update({'magic_url': re.sub('\&page=\d+|\?page=\d+\&', '',
                                                 self.context.get('magic_url'))})
        else:
            self.update_context(search_result=None)
            self.update_context(search_result_title='No matching records')
            self.update_context(count=0)

    def _get_search_models_prep(self):
        """Confirms self.get_search_models_prep returns a dictionary of format {\'model_name\': (app_label, model_name), ...}"""
        dct = self.get_search_models_prep()
        if not isinstance(dct, dict):
            raise TypeError('Method get_search_models_prep must return a dictionary. Got {0}'.format(dct))
        for k, v in dct.iteritems():
            if not isinstance(k, basestring):
                raise TypeError('Expected dictionary format {\'model_name\': (app_label, model_name), ...}. Got {0}'.format(dct))
            if not isinstance(v, tuple):
                raise TypeError('Expected dictionary format {\'model_name\': (app_label, model_name), ...}. Got {0}'.format(dct))
            if not get_model(v[0], v[1]):
                raise TypeError('Dictionary key, value must have a value tuple that returns a model class using get_model. Failed on get_model({1}, {2}). Got {0}'.format(dct, v[0], v[1]))
        return dct

    def get_search_prep_models(self):
        raise ImproperlyConfigured('Method name has changed to \'get_search_models_prep\'. Please update your code.')

    def get_search_models_prep(self):
        """ Users should override this to define custom search models. """
        return {'registeredsubject': ('bhp_registration', 'registeredsubject', None)}

    def _get_search_model(self, search_model_name):
        search_models = self._get_search_models_prep()
        try:
            app_label, model_name, section_name = search_models[search_model_name]
        except KeyError as e:
            raise KeyError('{0}. {1}'.format(e, 'Check that your url parameter \'search_name\' in the template url '
                                                'is the name of the model you are searching on and is a key in your '
                                                'search model map (see get_search_models_prep()).'))
        except:
            raise
        return get_model(app_label, model_name)

    def _get_search_result(self, request, search_name):
        if not search_name:
            raise AttributeError('Attribute \'search_name\' cannot be None. Call view() first.')
        return self.get_search_result(self, request, search_name)

    def get_search_result(self, request, search_name):
        """ Users should override this to define custom search logic. """
        search_result = None
        return search_result

    def _paginate(self, search_result, page=1, results_per_page=None):
        """Paginates the search result queryset after which templates
        access search_result.object_list.

        Also sets the 'magic_url' for previous/next paging urls

        Keyword Arguments:
            results_per_page: (default: 25)
        """
        if not results_per_page:
            results_per_page = 25
        if search_result:
            paginator = Paginator(search_result, results_per_page)
            try:
                search_result = paginator.page(page)
            except (EmptyPage, InvalidPage):
                search_result = paginator.page(paginator.num_pages)
        return search_result

    def hash_for_encrypted_fields(self, search_term, model_instance):
        """ Using the model's field objects and the search term, create a dictionary of
        {field_name, search term} where search term is hashed if this is an encrypted field """
        terms = {}
        for field in model_instance._meta.fields:
            if isinstance(field, BaseEncryptedField):
                # change the search term to a hash using the hasher on the field
                terms[field.attname] = field.field_cryptor.get_hash_with_prefix(search_term)
            else:
                # use the original search term
                terms[field.attname] = search_term
        return terms

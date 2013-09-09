import re
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model
from django import forms
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from bhp_crypto.fields import BaseEncryptedField
from bhp_search.exceptions import SearchError, SearchModelError, SearchAttributeError
from defaults import defaults
from patterns import patterns


class BaseSearch(object):

    """ Base search class. """

    APP_LABEL = 0
    MODEL_NAME = 1
    section = None
    search_model = None
    template = None
    order_by = None

    def __init__(self):
        self._section_name_list = None
        self._section = None
        self._section_name = None
        self._search_model_cls = None
        self._context = {}
        self._search_result_template = None
        self.form_is_valid = False
        self.registration_model = {}
        self.search_form = None
        self.search_label = None
        self.search_model_name = None
        self.pattern = patterns
        if 'name' not in dir(self):
            self.name = 'SEARCH'

    @property
    def context(self):
        return self._context

    def update_context(self, **kwargs):
        for k, v in kwargs.iteritems():
            self._context[k] = v

    def set_section(self):
        from bhp_section.classes import BaseSectionView
        self._section = self.section
        if not self._section:
            raise SearchAttributeError('Class attribute section may not be None for class {0}. Set this in the class declaration.'.format(self))
        if not issubclass(self._section, BaseSectionView):
            raise TypeError('Class attribute section must be a subclass of BaseSectionView for class {0}. Set this in the class declaration.'.format(self))

    def get_section(self):
        if not self._section:
            self.set_section()
        return self._section

    def set_section_name(self):
        self._section_name = self.get_section().section_name
        if not self._section_name:
            raise SearchAttributeError('Attribute \'section_name\' may not be None.')

    def get_section_name(self):
        if not self._section_name:
            self.set_section_name()
        return self._section_name

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
        self.context.update({'section_name': self.get_section_name()})
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

    def set_search_result_include_template(self, template=None):
        if template:
            self._search_result_template = template
        elif self.template:  # try for class attribute first
            self._search_result_template = self.template
        else:
            self._search_result_template = '{0}_include.html'.format(self.get_search_model_cls()._meta.object_name.lower())

    def get_search_result_include_template(self):
        if not self._search_result_template:
            self.set_search_result_include_template()
        return self._search_result_template

    def get_most_recent(self, page=1, limit=None):
        """Returns a queryset of the top most recent instances of the search model.

        Not technically a search function but it does use the other attributes like search_name...
        This is usually called from your section_index view."""
        if not limit:
            if 'MOST_RECENT_LIMIT' in dir(settings):
                limit = settings.MOST_RECENT_LIMIT
            else:
                limit = 15
        if limit > 0:
            model_cls = self.get_search_model_cls()
            return model_cls.objects.all().order_by('-created')[0:limit]
        return None

    def search(self, request, page=1, results_per_page=None):
        """
        Updates the context with the search results and has the queryset paginated.

        Keyword Arguments:
        search_result --
        """
        search_result = self._get_search_result(request)
        if search_result:
            # TODO: this does not make it to section (updated context etc.)
            count = search_result.count()
            paged_search_result = self._paginate(search_result, page, results_per_page)
            # Make sure page request is an int. If not, deliver first page.
            self.update_context(page=page)
            # If page request (9999) is out of range, deliver last page of results.
            self.update_context(search_result=paged_search_result)
            self.update_context(count=count)
            # remove page= from GET url
            self.context.update({'magic_url': re.sub('\&page=\d+|\?page=\d+\&', '',
                                                 self.context.get('magic_url'))})
        else:
            # TODO: this does not make it to section (updated context etc.)
            self.update_context(search_result=None)
            self.update_context(search_result_title='No matching records')
            self.update_context(count=0)
        return search_result

    def _set_search_model_cls(self, value=None):
        if self.search_model:
            if isinstance(self.search_model, tuple):
                self._search_model_cls = get_model(self.search_model[0], self.search_model[1])
            else:
                self._search_model_cls = self.search_model
        if not self._search_model_cls:
            raise SearchModelError('Attribute \'search_model_cls\' cannot be None')

    def get_search_model_cls(self):
        if not self._search_model_cls:
            self._set_search_model_cls()
        return self._search_model_cls

    def _get_search_result(self, request):
        return self.get_search_result(request)

    def get_search_result(self, request):
        """ Users should override this to define custom search logic. """
        raise ImproperlyConfigured('Method get_search_result must be overridden to return a search result based on criteria from the request object.')
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

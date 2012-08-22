import re
from django.shortcuts import render_to_response
#from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.db.models import get_model
from django.conf.urls.defaults import patterns as url_patterns, url
from django import forms
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from defaults import defaults
from patterns import patterns


class BaseSearch(object):

    """ Base search class. """

    def __init__(self, **kwargs):
        """
        Keyword Arguments:
        search_result_template --
        section_name --
        """
        self.ready = False
        self.registration_model = {}
        self.search_form = None
        self.search_model_name = None
        self.search_model = {}
        self._context = {}
        self.pattern = patterns

    @property
    def context(self):
        return self._context

    def update_context(self, **kwargs):
        for k, v in kwargs.iteritems():
            self._context[k] = v

    def urlpatterns(self, section_names, app_label='bhp_search', view=None):
        """ Generates a urlpattern for the view of this subclass."""
        if view is None:
            view = self.view
        urlpattern = url_patterns('{app_label}.views'.format(app_label=app_label),
             url(r'^(?P<section_name>{section_names})/search/(?P<search_name>\w+)/by(?P<search_by>{search_type})/$'.format(section_names='|'.join(section_names), search_type=self.search_type),
            self.view,
            name="section_search_by_url_name"))
        return urlpattern

    #@login_required
    def view(self, request, **kwargs):
        """Renders the view."""
        self._context = {}
        self.prepare(request, **kwargs)
        self.prepare_form(request, **kwargs)
        if self.ready:
            #form is ready or "is_valid() = True", so get the search result
            self.search(request, **kwargs)
        return render_to_response(
                  self.context.get('template'),
                  self.context,
                  context_instance=RequestContext(request))

#    def update_context_with_most_recent(self, request, **kwargs):
#        model = self.get_search_model(kwargs.get('search_name'))
#        search_result = model.objects.all().order_by('-created')[0:10]
#        self.update_result_to_context(request, search_result)

    def prepare(self, request, **kwargs):

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
        self.context.update({'report_title': 'Search {0} by {1}'.format(self.context.get('search_name'), self.search_type)})
        self.context.update({'extend': 'base_search_by_{0}.html'.format(self.search_type)})
        self.context.update({'search_by_name': self.search_type})
        self.context.update({'section_name': kwargs.get('section_name')})
        if request.method == 'POST':
            self.update_context(magic_url=request.POST.urlencode())
        elif request.method == 'GET':
            if request.POST.urlencode():
                self.update_context(magic_url=request.GET.urlencode())

    def prepare_form(self, request, **kwargs):
        """ Updates the context with the search form and updates
        the search form with POST or GET. """
        # setup the search form
        self.ready = False
        if not issubclass(self.search_form, forms.Form):
            raise TypeError('Expected subclass of forms.Form. Got {0}'.format(self.search_form))
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
                self.ready = True
        else:
            self.update_context(form=self.search_form())

    def get_most_recent(self, model_name=None, page=1, limit=15):
        if model_name:
            model = self.get_search_model(model_name)
            search_result = model.objects.all()[0:limit]
            return self._paginate(search_result, page)
        return None

    def search(self, request, **kwargs):
        """
        Updates the context with the search results and has the queryset paginated.

        Keyword Arguments:
        search_result --
        """
        search_result = self.get_search_prep(request, **kwargs)
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

    def get_search_prep_models(self):
        """ Users should override this to define custom search models. """
        return {'registeredsubject': ('bhp_registration', 'registeredsubject')}

    def get_search_model(self, search_model_name):
        search_models = self.get_search_prep_models()
        try:
            (app_label, model_name) = search_models[search_model_name]
        except KeyError as e:
            raise KeyError('{0}. {1}'.format(e, 'Check that your url parameter \'search_name\' in the template url '
                                                'is the name of the model you are searching on and is a key in your '
                                                'search model map (see get_search_prep_models()).'))
        except:
            raise
        return get_model(app_label, model_name)

    def get_search_prep(self, request, **kwargs):
        """ Users should override this to define custom search logic. """
        search_result = None
        return search_result

    def _paginate(self, search_result, page=1, **kwargs):
        """Paginates the search result queryset after which templates
        access search_result.object_list.

        Also sets the 'magic_url' for previous/next paging urls

        keyword Arguments:
        results_per_page -- (default: 25)
        """
        if search_result:
            results_per_page = kwargs.get('results_per_page', 25)
            paginator = Paginator(search_result, results_per_page)
            try:
                search_result = paginator.page(page)
            except (EmptyPage, InvalidPage):
                search_result = paginator.page(paginator.num_pages)
        return search_result

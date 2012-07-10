import re
from django.conf.urls.defaults import patterns as url_patterns, url
from django import forms
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from defaults import defaults
from patterns import patterns


class BaseSearch(object):
    
    def __init__(self, request, search_type, **kwargs):
        self.ready = False
        self.search_type = search_type # (word, date, week)
        self.registration_model = {}
        self.search_form=None
        self.search_model_name=None
        self.search_model={}
        self._context={}
        self.update_context(**defaults)
        self.pattern=patterns
        #search_name: comes as a parameter from the Url
        if not kwargs.get('search_name', None):
            raise TypeError('BaseSearch requires keyword/value for key \'search_name\'. None given.')
        else:
            self.context.update({'search_name':kwargs.get('search_name')})
            self.search_model_name = kwargs.get('search_name')
        # search_result_template: if you look at the base_search.html you'll see that 
        # the result set block refers to an include file.  
        if not kwargs.get('search_result_template', None):
            self.context.update({'search_result_template':'{0}_include.html'.format(self.context.get('search_name'))})
        else:
            self.context.update({ 'search_result_template': kwargs.get('search_result_template')})   
            
        # check **kwargs for queryset_label, otherwise default
        self.context.update({'queryset_label':kwargs.get('queryset_label', '{0}_by_{1}'.format(self.context.get('search_name'), self.search_type))})
        self.context.update({'report_title':'Search {0} by {1}'.format(self.context.get('search_name'), self.search_type)})
        self.context.update({'extend':'base_search_by_{0}.html'.format(self.search_type)}) 
        self.context.update({'search_by_name': self.search_type})
        self.context.update({'section_name':kwargs.get('section_name')})       
                    
    @property
    def context(self): 
        return self._context

    def update_context(self, **kwargs):
        for k,v in kwargs.iteritems():
            self._context[k]=v
    
    @classmethod
    def urlpatterns(self, views, section_names):
        urlpattern=url_patterns(views, 
             url(r'^(?P<section_name>{section_names})/search/(?P<search_name>\w+)/by(?P<search_by>word)/$'.format(section_names='|'.join(section_names)),
            'search_response', 
            name="section_search_by_url_name"))
        return urlpattern
    
    def prepare(self, request):
        if request.method == 'POST':
            self.update_context(magic_url=request.POST.urlencode())                
        elif request.method == 'GET':    
            if request.POST.urlencode():
                self.update_context(magic_url=request.GET.urlencode())
    
    def prepare_form(self, request, **kwargs):
        # setup the search form
        self.ready=False
        if not issubclass(self.search_form, forms.Form):
            raise TypeError('Expected subclass of forms.Form. Got {0}'.format(self.search_form))
        if ((request.method == 'GET' and not request.GET == {}) or ( request.method == 'POST' and not request.POST == {})):            
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
                self.update_context(search_term=self.context.get('form').cleaned_data.get('search_term'))
                self.update_context(search_result_title='Results for search term \'{0}\''.format(self.context.get('search_term')))              
                self.ready=True
        else:     
            self.update_context(form=self.search_form())
    
    def search(self, request, **kwargs):
        raise TypeError("BaseSearch.get_labeled_queryset must be overridden by child class")      
    
    def paginate(self, page=1):
        search_result=self.context.get('search_result')
        if search_result:
            paginator=Paginator(search_result, 25)                                    
            # Make sure page request is an int. If not, deliver first page.
            self.update_context(page=page)
            # If page request (9999) is out of range, deliver last page of results.
            try:
                self.update_context(search_result=paginator.page(self.context.get('page')))
            except (EmptyPage, InvalidPage):
                self.update_context(search_result=paginator.page(paginator.num_pages))
        # remove page= from GET url
        self.context.update({'magic_url': re.sub('\&page=\d+|\?page=\d+\&' , '' , self.context.get('magic_url')) })

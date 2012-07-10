import re
from django.conf.urls.defaults import patterns as url_patterns, url
from django import forms
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from defaults import defaults
from patterns import patterns


class BaseSearch(object):
    
    def __init__(self, request, **kwargs):
        self.ready = False
        self.registration_model = {}
        self.search_form=None
        self.search_model_name=None
        self.search_model={}
        self._context={}
        self.update_context(**defaults)
        self.pattern=patterns
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
    def urlpatterns(self, section_names, app_label='bhp_search',view='search'):
        #urlpatterns=url_patterns('{app_label}.views'.format(app_label=app_label), 
                                 
        urlpattern=url_patterns('{app_label}.views'.format(app_label=app_label), 
             url(r'^(?P<section_name>{section_names})/search/(?P<search_name>\w+)/by(?P<search_by>{search_type})/$'.format(section_names='|'.join(section_names), search_type=self.search_type),
            view, 
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
                self.ready=True
        else:     
            self.update_context(form=self.search_form())
    
    def search(self, request, **kwargs):
        search_result=kwargs.get('search_result')
        self.update_context(count=0)
        if search_result:
            self.paginate(request.GET.get('page', '1'))    
            self.update_context(search_result=search_result)
            self.update_context(count=search_result.count())
        else:
            self.update_context(search_result_title='No matching records') 
    
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

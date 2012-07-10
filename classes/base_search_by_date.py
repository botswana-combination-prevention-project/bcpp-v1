from django.utils.translation import ugettext_lazy as _
from base_search import BaseSearch


class BaseSearchByDate(BaseSearch):
    """ subclass of BaseSearch specfic to date range search"""
    def __init__(self, request, **kwargs):
        
        BaseSearch.__init__(self, request, **kwargs )

    def get_response(self, request, **kwargs):
        
        self['report_title'] = "Search %s by date range" % (self['search_name'])
        
        #may wish to handlethis as kwargs
        self['search_helptext'] = _(u'Search by date range')
        self['extend'] = "base_search_by_date.html" 
        self['search_by_name'] = 'date'           
            
        # check **kwargs for queryset_label, otherwise default
        if not kwargs.get('queryset_label') is None:
            self['queryset_label'] = kwargs.get('queryset_label')
        else:
            self['queryset_label'] = self['search_name']          
        if ((request.method == 'GET' and not request.GET == {}) or ( request.method == 'POST' and not request.POST == {})):            
            if request.method == 'POST':
                self['form'] = self.form(request.POST)                  
            elif request.method == 'GET':    
                self['form'] = self.form(request.GET)                  
            else:
                raise TypeError('Request method unknown. Expected POST or GET. See BaseSearchByWeek')

            if self['form'].is_valid():
                
                if request.method == 'POST':
                    self['magic_url'] = request.POST.urlencode()                
                elif request.method == 'GET':    
                    self['magic_url'] = request.GET.urlencode()                


                self['date_start'] = "%s 00:00" % (self['form'].cleaned_data['date_start'])
                self['date_end'] = "%s 23:59" % (self['form'].cleaned_data['date_end'])
                        
                self['search_result_title'] = 'Results for period from %s to %s.' % (self['date_start'], self['date_end'] )                               

                """this will be overridden in the subclass"""
                self.get_labeled_queryset(
                    self['queryset_label'], 
                    date_start=self['date_start'],
                    date_end=self['date_end'], 
                    cleaned_data=self['form'].cleaned_data 
                    )                       
        else:     
    
            if kwargs.get('date_start') and kwargs.get('date_end'):
                data = {}
                for k,v in kwargs.items():
                    data[k]=v
                #data['date_start'] = kwargs.get('date_start')
                #data['date_end'] = kwargs.get('date_end')

                self['form'] = self.form(data)                      
            else:
                self['form'] = self.form()  
        return 




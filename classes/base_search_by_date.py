from django.utils.translation import ugettext_lazy as _
from bhp_search.forms import DateRangeSearchForm
from base_search import BaseSearch

class BaseSearchByDate(BaseSearch):
    """ subclass of BaseSearch specfic to date range search"""
    def __init__(self, request, **kwargs):
        
        BaseSearch.__init__(self, request, **kwargs )
        
        self['report_title'] = "Search %s by date range" % (self['section_name'])
        
        #may wish to handlethis as kwargs
        self['search_helptext'] = _(u'Search by date range. Dates are based on the date created. ')
        self['extend'] = "base_search_by_date.html" 
        self['search_by_name']='date'           
            
        # check **kwargs for queryset_label, otherwise default
        if not kwargs.get('queryset_label') is None:
            self['queryset_label'] = kwargs.get('queryset_label')
        else:
            #self['queryset_label'] = '%s_by_date' % (self['search_name'])
            self['queryset_label'] = self['search_name']            

        if request.method == 'POST':            
            self['form'] = DateRangeSearchForm(request.POST)
            if self['form'].is_valid():
                self['date_start']= self['form'].cleaned_data['date_start']
                self['date_end']= self['form'].cleaned_data['date_end']                
                self['search_result_title'] = 'Results for period from %s to %s.' % (self['date_start'], self['date_end'] )                               

                """this will be overridden in the subclass"""
                self.get_labeled_queryset(self['queryset_label'], date_start=self['date_start'],date_end=self['date_end'] )                       
        else:     
            self['form'] = DateRangeSearchForm()
    
        return 




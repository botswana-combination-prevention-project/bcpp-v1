from django.utils.translation import ugettext_lazy as _
from bhp_search.utils import weekBoundaries
from bhp_search.forms import WeekNumberSearchForm
from base_search import BaseSearch


class BaseSearchByWeek(BaseSearch):
    """ subclass of BaseSearch specfic to week number range search"""
    def __init__(self, request, **kwargs):

        BaseSearch.__init__(self, request, **kwargs )
        
        self['report_title'] = "Search %s by week number" % (self['search_name'])
        #may wish to handlethis as kwargs
        self['search_helptext'] = _(u'Search by week number. Week number is based on the date created. ')
        self['extend'] = "base_search_by_date.html"
        self['search_by_name']='week'        

        # check **kwargs for queryset_label, otherwise default
        if not kwargs.get('queryset_label') is None:
            self['queryset_label'] = kwargs.get('queryset_label')
        else:
            #self['queryset_label'] = '%s_by_week' % (self['search_name'])
            self['queryset_label'] = self['search_name']

        if ((request.method == 'GET' and not request.GET == {}) or ( request.method == 'POST' and not request.POST == {})):            
            if request.method == 'POST':
                self['form'] = WeekNumberSearchForm(request.POST)
            elif request.method == 'GET':    
                self['form'] = WeekNumberSearchForm(request.GET)
            else:
                raise TypeError('Request method unknown. Expected POST or GET. See BaseSearchByWeek')
                    
            if self['form'].is_valid() :
                
                if request.method == 'POST':
                    self['magic_url'] = request.POST.urlencode()                
                elif request.method == 'GET':    
                    self['magic_url'] = request.GET.urlencode()                

                
                week_start=self['form'].cleaned_data['date_start']
                week_end=self['form'].cleaned_data['date_end']
                year = int(self['form'].cleaned_data['year'])
                
                #this form returns week numbers so convert to datetime
                wb_start = weekBoundaries(year, int(week_start))
                wb_end = weekBoundaries(year, int(week_end))
                
                if week_start == week_end:
                    self['week_range']="week %s" % (week_start)
                else:
                    self['week_range']="weeks %s to %s" % (week_start, week_end)   
                 
                self['date_start'] = "%s 00:00" % (wb_start[0])
                self['date_end']= "%s 23:59" % (wb_end[1])          
                self['search_term'] = 'from %s to %s' % (self['date_start'], self['date_end'] )  
                self['search_result_title'] = 'Results for %s : (period from %s to %s).' % (self['week_range'], self['date_start'], self['date_end'] )               
                
                self.get_labeled_queryset(self['queryset_label'], date_start=self['date_start'],date_end=self['date_end'] )                       
        else:     
            self['form'] = WeekNumberSearchForm()
                     
        return 




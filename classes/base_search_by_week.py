from datetime import date, timedelta
from django.db.models import Q
from bhp_search.forms import WeekYearSearchForm
from base_search import BaseSearch


class BaseSearchByWeek(BaseSearch):

    search_type='week'
    
    def __init__(self, request, **kwargs):
        
        super(BaseSearchByWeek, self).__init__(request, **kwargs )
        defaults = {'search_helptext':'Search by date.'}
        self.search_form = WeekYearSearchForm 
        self.context.update(**defaults) 

    def prepare_form(self, request, **kwargs):
        super(BaseSearchByWeek, self).prepare_form(request, **kwargs )
        #self.update_context(search_result_    title='Results for \'{0}\''.format([v for v in self.context.get('form').cleaned_data.itervalues()]))  
        #self['search_result_title'] = 'Results for period from %s to %s.' % (self['date_start'], self['date_end'] )                               

    
    def search(self, request, **kwargs):                       

        model=self.search_model.get(self.search_model_name)
        
        
        #this form returns week numbers so convert to datetime
        wb_start = self.weekBoundaries(self.context.get('form').cleaned_data.get('year_start'), int(self.context.get('form').cleaned_data.get('week_start')))
        wb_end = self.weekBoundaries(self.context.get('form').cleaned_data.get('year_end'), int(self.context.get('form').cleaned_data.get('week_end')))
                        
        qset_created=Q(Q(created__gte="%s 00:00" % (wb_start[0])),
                       Q(created__lte="%s 23:59" % (wb_end[1])))
        qset_modified=Q(Q(modified__gte="%s 00:00" % (wb_start[0])),
                        Q(modified__lte="%s 23:59" % (wb_end[1])))                     
        search_result=model.objects.filter(qset_created | qset_modified).order_by('-created')
        kwargs.update({'search_result':search_result})
        super(BaseSearchByWeek, self).search(request, **kwargs)


    def weekBoundaries(self, year, week):
        """http://bytes.com/topic/python/answers/499819-getting-start-end-dates-given-week-number"""
        startOfYear = date(year, 1, 1)
        now = startOfYear + timedelta(weeks=week)
        # isoweekday() % 7 returns Sun=0 ... Sat=6
        sun = now - timedelta(days=now.isoweekday() % 7)
        sat = sun + timedelta(days=6)
        #if DEBUG:
        #    print "DEBUG: now = %s/%s" % (now, now.strftime("%a"))
        #    print "DEBUG: sun = %s/%s" % (sun, sun.strftime("%a"))
        #    print "DEBUG: sat = %s/%s" % (sat, sat.strftime("%a"))
        return sun, sat
    
    
    
#    def __init__(self, request, **kwargs):
#
#        BaseSearch.__init__(self, request, **kwargs )
#        
#        self['report_title'] = "Search %s by week number" % (self['search_name'])
#        #may wish to handlethis as kwargs
#        self['search_helptext'] = _(u'Search by week number. Week number is based on the date created. ')
#        self['extend'] = "base_search_by_date.html"
#        self['search_by_name']='week'        
#
#        # check **kwargs for queryset_label, otherwise default
#        if not kwargs.get('queryset_label') is None:
#            self['queryset_label'] = kwargs.get('queryset_label')
#        else:
#            #self['queryset_label'] = '%s_by_week' % (self['search_name'])
#            self['queryset_label'] = self['search_name']
#
#        if ((request.method == 'GET' and not request.GET == {}) or ( request.method == 'POST' and not request.POST == {})):            
#            if request.method == 'POST':
#                self['form'] = WeekNumberSearchForm(request.POST)
#            elif request.method == 'GET':    
#                self['form'] = WeekNumberSearchForm(request.GET)
#            else:
#                raise TypeError('Request method unknown. Expected POST or GET. See BaseSearchByWeek')
#                    
#            if self['form'].is_valid() :
#                
#                if request.method == 'POST':
#                    self['magic_url'] = request.POST.urlencode()                
#                elif request.method == 'GET':    
#                    self['magic_url'] = request.GET.urlencode()                
#
#                
#                week_start=self['form'].cleaned_data['date_start']
#                week_end=self['form'].cleaned_data['date_end']
#                year = int(self['form'].cleaned_data['year'])
#                
#                #this form returns week numbers so convert to datetime
#                wb_start = weekBoundaries(year, int(week_start))
#                wb_end = weekBoundaries(year, int(week_end))
#                
#                if week_start == week_end:
#                    self['week_range']="week %s" % (week_start)
#                else:
#                    self['week_range']="weeks %s to %s" % (week_start, week_end)   
#                 
#                self['date_start'] = "%s 00:00" % (wb_start[0])
#                self['date_end']= "%s 23:59" % (wb_end[1])          
#                self['search_term'] = 'from %s to %s' % (self['date_start'], self['date_end'] )  
#                self['search_result_title'] = 'Results for %s : (period from %s to %s).' % (self['week_range'], self['date_start'], self['date_end'] )               
#                
#                self.get_labeled_queryset(self['queryset_label'], date_start=self['date_start'],date_end=self['date_end'] )                       
#        else:     
#            self['form'] = WeekNumberSearchForm()
#                     
#        return 
#
#


import inspect
from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models import Q


class VisitDefinitionManager(models.Manager):
    
    """
schedule_group=ScheduleGroup.objects.all()
schedule_group=schedule_group[4]
visit_definition = VisitDefinition.objects.filter(code='2010',schedule_group=schedule_group).order_by('time_point')[0]
VisitDefinition.objects.next_visit_definition(visit_definition=visit_definition)
    """
    
    
    def next_visit_definition(self, **kwargs):

        """ return next visit_definition for the given visit_definition """        

        if kwargs.get('visit_definition'):
            visit_definition = kwargs.get('visit_definition')
            schedule_group = visit_definition
            #if not isinstance(visit_definition, super(VisitDefinitionManager, self)):
            #    raise AttributeError, '%s method %s requires visit_definition to be an instance of VisitDefintion' %  (self.__name__, inspect.stack()[0][3],)
        elif kwargs.get('schedule_group') and kwargs.get('code'):
            schedule_group = kwargs.get('schedule_group')       
            code = kwargs.get('code')       
            if super(VisitDefinitionManager, self).filter(schedule_group=schedule_group, code=code):
                visit_definition = super(VisitDefinitionManager, self).get(schedule_group=schedule_group, code=code)
            else:
                raise ValueError, '%s method %s cannot determine the visit_definition given schedule_group=\'%s\' and code=\'%s\''   % (self.__name__, inspect.stack()[0][3],schedule_group, code,)
        else:
            raise AttributeError, '%s method %s requires a visit_definition instance OR schedule_group and code' % (self.__name__, inspect.stack()[0][3], )             

        visit_definitions = super(VisitDefinitionManager, self).filter(schedule_group=visit_definition.schedule_group).exclude(id=visit_definition.id).order_by('time_point') 

        if visit_definitions:
            next_visit_def = visit_definitions[0]
        else:
            next_visit_def = None
        return next_visit_def
        
    def relativedelta_from_base(self, **kwargs):        
    
        """ return the relativedelta from the zero time_point visit_definition """

        if kwargs.get('visit_definition'):
            visit_definition = kwargs.get('visit_definition')
        else:
            raise AttributeError, '%s method %s requires a visit_definition instance' % (self.__name__, inspect.stack()[0][3], )             

        interval = visit_definition.base_interval
        unit = visit_definition.base_interval_unit
        if interval == 0:
            rdelta = relativedelta(days=0)
        else:    
            if unit == 'Y':
                rdelta = relativedelta(years=interval)
            elif unit == 'M':
                rdelta = relativedelta(months=interval)        
            elif unit == 'D':
                rdelta = relativedelta(days=interval)        
            elif unit == 'H':        
                rdelta = relativedelta(hours=interval)
            else:
                raise AttributeError, "Cannot calculate relativedelta, visit_definition.base_interval_unit must be Y,M,D or H. Got %s" % (unit,)  
        return rdelta                     

        
        
        


def release_auto_from_dmis():
    import pyodbc, datetime
    from django.db.models import Avg, Max, Min, Count
    from lab_result.models import Result, ResultSource
    from lab_result_item.models import ResultItem
   
    # update NT AUTHORITY username to 'auto' for any result_item
    ResultItem.objects.filter(result_item_operator__icontains='AUTHORITY').update(result_item_operator='auto')

    #unrelease everything
    Result.objects.all().update(release_status='NEW')       

    oResults = Result.objects.filter(release_status__exact='NEW')
    
    for oResult in oResults:
        #get max validation datetime
        aggr = ResultItem.objects.filter(result=oResult, validation_status__exact='F',).aggregate(Max('validation_datetime'),)
        if aggr['validation_datetime__max']:
            validation_datetime = aggr['validation_datetime__max']
            #get validation_username for that validation_datetime
            validation_username = ResultItem.objects.filter(result=oResult, validation_status__exact='F', validation_datetime__exact=validation_datetime)[0].validation_username        
            if validation_username == 'auto':
                validation_username = unicode('smoyo')
            # update result    
            oResult.release_status = 'RELEASED'
            oResult.release_datetime = validation_datetime
            oResult.release_username = validation_username
            oResult.save()    
            

if __name__ == "__main__":
    
    import sys,os
    sys.path.append('/home/django/source/')
    sys.path.append('/home/django/source/bhplab/')
    os.environ['DJANGO_SETTINGS_MODULE'] ='bhplab.settings'
    from django.core.management import setup_environ
    from bhplab import settings

    setup_environ(settings)
    
    print 'release \'auto\' from dmis....'
    release_auto_from_dmis()
    print 'Done'
    sys.exit (0) 

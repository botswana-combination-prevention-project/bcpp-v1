from datetime import date, datetime
from lab_clinic_api.models import Lab, Result, ResultItem, UpdateLog
from lab_clinic_api.classes import ResultContext, LabContext
from lab_import_dmis.classes import Dmis, DmisReceive


def update_results(subject_identifier=None):
    if subject_identifier:            
        dmis = Dmis()
        dmis.fetch(subject_identifier=subject_identifier, lab_db='lab_api')
        dmis = DmisReceive()
        dmis.fetch(subject_identifier=subject_identifier, lab_db='lab_api')
        dmis = DmisOrder()
        dmis.fetch(subject_identifier=subject_identifier, lab_db='lab_api')
        labs = Lab.objects.fetch(subject_identifier=subject_identifier)
        if labs:
            results = Result.objects.fetch(subject_identifier=subject_identifier, labs=labs)
            if results:
                ResultItem.objects.fetch(subject_identifier=subject_identifier, results=results)        
        if Lab.objects.filter(subject_identifier=subject_identifier, result__isnull=True):
            Lab.objects.filter(subject_identifier=subject_identifier, result__isnull=True).delete()        
    return subject_identifier            
                

    


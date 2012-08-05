#from datetime import date, datetime
from lab_clinic_api.models import Lab, Result, ResultItem
#from lab_clinic_api.classes import ResultContext, LabContext
#from lab_import_dmis.classes import Dmis, DmisReceive, DmisOrder

"""

from lab_clinic_api.classes import DmisResults
dmis_results = DmisResults()
for rs in RegisteredSubject.objects.filter(subject_type='infant'):
    dmis_results.subject_identifier=rs.subject_identifier
    dmis_results.fetch()
    rs.subject_identifier

"""


class DmisResults(object):

    subject_identifier = None

    def fetch(self):
        if self.subject_identifier:
            #dmis = Dmis()
            #dmis.fetch(subject_identifier=self.subject_identifier, lab_db='lab_api')
            ###dmis = DmisReceive()
            #dmis.fetch(subject_identifier=self.subject_identifier, lab_db='lab_api')
            #dmis = DmisOrder()
            #dmis.fetch(subject_identifier=self.subject_identifier, lab_db='lab_api')
            labs = Lab.objects.fetch(subject_identifier=self.subject_identifier)
            if labs:
                results = Result.objects.fetch(subject_identifier=self.subject_identifier, labs=labs)
                if results:
                    ResultItem.objects.fetch(subject_identifier=self.subject_identifier, results=results)
            if Lab.objects.filter(subject_identifier=self.subject_identifier, result__isnull=True):
                Lab.objects.filter(subject_identifier=self.subject_identifier, result__isnull=True).delete()

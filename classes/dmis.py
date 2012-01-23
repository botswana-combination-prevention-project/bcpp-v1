
from dmis_receive import DmisReceive
from dmis_order import DmisOrder
from dmis_result import DmisResult
from dmis_validation import DmisValidation
from dmis_release import DmisRelease

class Dmis(object):
    
    def __init__(self, debug=False):
        
        self.debug = debug
        
    def fetch(self, **kwargs):
        
        self.lab_db = kwargs.get('lab_db', 'default')
        self.subject_identifier = kwargs.get('subject_identifier')
        
        dmis = DmisReceive(debug=self.debug)
        dmis.fetch(subject_identifier=self.subject_identifier, lab_db=self.lab_db)
                
        dmis = DmisOrder(debug=self.debug)
        dmis.fetch(subject_identifier=self.subject_identifier, lab_db=self.lab_db)
        
        dmis = DmisResult(debug=self.debug)
        dmis.fetch(subject_identifier=self.subject_identifier, lab_db=self.lab_db)

        dmis = DmisValidation(debug=self.debug)
        dmis.fetch(subject_identifier=self.subject_identifier, lab_db=self.lab_db)

        dmis = DmisRelease(debug=self.debug)
        dmis.release(subject_identifier=self.subject_identifier, lab_db=self.lab_db)
        

#from django.db import models
#from audit_trail.audit import AuditTrail
from bhp_base_model.classes import BaseModel
from bhp_crypto.fields import EncryptedCharField, EncryptedTextField, EncryptedFirstnameField, EncryptedLastnameField


class TestModel(BaseModel):     
            
    firstname = EncryptedFirstnameField()
    
    lastname = EncryptedLastnameField()
    
    char1 = EncryptedCharField()
    
    char2 = EncryptedCharField()
    
    text1 = EncryptedTextField()
    
    text2 = EncryptedTextField()

    text3 = EncryptedTextField()

    #history=AuditTrail()

    def get_subject_identifier(self):
        return ''

    class Meta:
        app_label='bhp_crypto'


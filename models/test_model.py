#from django.db import models
from audit_trail.audit import AuditTrail
from bhp_base_model.models import BaseModel
from bhp_crypto.fields import EncryptedCharField, EncryptedTextField, EncryptedFirstnameField, EncryptedLastnameField


class TestModel(BaseModel):

    firstname = EncryptedFirstnameField()

    lastname = EncryptedLastnameField()

    char1 = EncryptedCharField()

    lastname2 = EncryptedLastnameField()

    char2 = EncryptedCharField()

    text1 = EncryptedTextField()

    char3 = EncryptedCharField()

    text2 = EncryptedTextField()

    firstname2 = EncryptedFirstnameField()

    text3 = EncryptedTextField()

    history = AuditTrail(show_in_admin=True)

    def get_subject_identifier(self):
        return ''

    class Meta:
        app_label = 'bhp_crypto'

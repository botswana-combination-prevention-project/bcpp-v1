from django.db import models


class PatientManager(models.Manager):
    
    def check_accounts(self):
        pass
        
    def check_consent(self):
        pass


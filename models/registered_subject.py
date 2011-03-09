from django.db import models
from base_subject import BaseSubject

class RegisteredSubject(BaseSubject):

    pass

    def __unicode__ (self):
        return "%s %s (%s)" % (self.subject_identifier, self.subject_type, self.first_name)

    class Meta:
        app_label = 'bhp_registration'            


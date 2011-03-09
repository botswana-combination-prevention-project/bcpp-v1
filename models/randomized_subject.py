from django.db import models
from base_subject import BaseSubject

class RandomizedSubject(BaseSubject):

    pass

    def __unicode__ (self):
        return "%s %s" % (self.subject_identifier, self.subject_type)


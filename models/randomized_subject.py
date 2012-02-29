from base_subject import BaseSubject

class RandomizedSubject(BaseSubject):


    def __unicode__ (self):
        return "%s %s" % (self.subject_identifier, self.subject_type)

    class Meta:
        app_label = 'bhp_registration'           


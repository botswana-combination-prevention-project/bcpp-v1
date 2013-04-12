from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bhp_botswana.models import BaseBwConsent


class SubjectConsent(BaseBwConsent):

    history = AuditTrail()
    
    objects = models.Manager()

    def __unicode__(self):
        return "{0} {1} {2} ({3}) born {4}".format(self.subject_identifier,
                                          self.first_name, self.last_name,
                                          self.initials, self.dob.isoformat())
        
    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_subjectconsent_change', args=(self.id,))

    def get_subject_type(self):
        return 'subject'

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = 'Subject Consent'

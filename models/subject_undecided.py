from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from base_member_status_model import BaseMemberStatusModel


class SubjectUndecided (BaseMemberStatusModel):
    
    history = AuditTrail()
    
    
    def get_absolute_url(self):
        if self.id:
            return reverse('admin:bcpp_subject_subjectundecided_change', args=(self.id,))
        else:
            return reverse('admin:bcpp_subject_subjectundecided_add')
        
    
    def member_status_string(self):
        return 'UNDECIDED'
    
    
    def save(self, *args, **kwargs):
        self.survey = self.household_member.survey
        super(SubjectUndecided, self).save(*args, **kwargs)


    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Subject Undecided"
        verbose_name_plural = "Subject Undecided"
        unique_together = ('registered_subject', 'survey',)

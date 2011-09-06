from django.db import models
from bhp_common.models import MyBasicUuidModel
from audit_trail.choices import AUDITCODES


class AuditComment (MyBasicUuidModel):

    app_label = models.CharField(
        max_length=35,
        )

    model_name = models.CharField(
        max_length=50,
        )

    audit_subject_identifier = models.CharField(
        max_length=50,
        )

    audit_id = models.IntegerField(
        db_index = True)
    
    audit_code = models.CharField(
        max_length = 25,
        choices = AUDITCODES,
        )

    audit_comment = models.TextField(
        max_length = 250,
        help_text = 'Add a comment describing the reason for the data change.'
        )

    def __unicode__(self):
        return self.audit_comment[0:50]

    class Meta:
        app_label = 'audit_trail'  
        ordering = ['audit_id','created']      
    

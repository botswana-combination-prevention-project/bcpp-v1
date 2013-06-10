from django.db import models
from bhp_base_model.models import BaseUuidModel
from bhp_base_model.fields import MyUUIDField
from audit_trail.choices import AUDITCODES


class AuditComment (BaseUuidModel):

    app_label = models.CharField(
        max_length=35,
        )

    model_name = models.CharField(
        max_length=50,
        )

    audit_subject_identifier = models.CharField(
        max_length=50,
        )

    audit_id = MyUUIDField(
        db_index=True,
        editable=True)

    audit_code = models.CharField(
        max_length=25,
        choices=AUDITCODES,
        )

    audit_comment = models.TextField(
        max_length=250,
        help_text='Add a comment describing the reason for the data change.'
        )

    def __unicode__(self):
        return self.audit_comment[0:50]

    class Meta:
        app_label = 'audit_trail'
        ordering = ['created']

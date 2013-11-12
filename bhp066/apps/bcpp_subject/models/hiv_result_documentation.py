from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import date_not_future

from apps.bcpp.choices import RECORDEDHIVRESULT_CHOICE

from ..choices import HIV_DOC_TYPE
from .base_scheduled_visit_model import BaseScheduledVisitModel


class HivResultDocumentation (BaseScheduledVisitModel):

    """CS002 - for usage only and if only patient has other result for HIV"""

    result_date = models.DateField(
        verbose_name=("What is the recorded date of this previous HIV test (or of the document that provides supporting evidence of HIV infection)?"),
        validators=[date_not_future],
        help_text="",
        )

    result_recorded = models.CharField(
        verbose_name=("What is the recorded HIV status indicated by this additional document?"),
        max_length=30,
        choices=RECORDEDHIVRESULT_CHOICE,
        help_text="",
        )

    result_doc_type = models.CharField(
        verbose_name=("What is the type of document used?"),
        max_length=35,
        choices=HIV_DOC_TYPE,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV result documentation"
        verbose_name_plural = "HIV result documentation"

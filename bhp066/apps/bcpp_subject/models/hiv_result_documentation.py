from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import datetime_not_future

from apps.bcpp.choices import RECORDEDHIVRESULT_CHOICE

from ..choices import HIV_DOC_TYPE
from .base_scheduled_visit_model import BaseScheduledVisitModel


class HivResultDocumentation (BaseScheduledVisitModel):

    """CS002 - for usage only and if only patient has other result for HIV"""

    result_date = models.DateTimeField(                         
        verbose_name=_("What is the recorded date of the HIV test?"),
        validators = [datetime_not_future], 
        help_text="",
        )

    result_recorded = models.CharField(
        verbose_name=_("What is the recorded HIV test result?"),
        max_length=30,
        choices=RECORDEDHIVRESULT_CHOICE,
        help_text="",
        )

    result_doc_type = models.CharField(
        verbose_name=_("What is the type of document used?"),
        max_length=35,
        choices=HIV_DOC_TYPE,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV result documentation"
        verbose_name_plural = "HIV result documentation"

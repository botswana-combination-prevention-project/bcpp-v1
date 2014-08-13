from datetime import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import date_not_future

from apps.bcpp.choices import RECORDEDHIVRESULT_CHOICE

from .base_scheduled_visit_model import BaseScheduledVisitModel
# from ..constants import RBD


class HivTestReview (BaseScheduledVisitModel):

    """Complete this form if HivTestingHistory.has_record."""

    hiv_test_date = models.DateField(
        verbose_name=_("What was the recorded date of the last HIV test?"),
        validators=[date_not_future],
        help_text="Obtain this information from the card the participant presents to you.",
        )

    recorded_hiv_result = models.CharField(
        verbose_name=_("What was the recorded HIV test result?"),
        max_length=30,
        choices=RECORDEDHIVRESULT_CHOICE,
        help_text=_("If the participant and written record differ, the result"
                   " from the written record should be recorded."),
        )

    history = AuditTrail()

    def save(self, *args, **kwargs):
#         self.validate_participation_type(self)
        super(HivTestReview, self).save(*args, **kwargs)

#     def validate_participation_type(self, hiv_test_review, exception_cls=None):
#         exception_cls = exception_cls or ValidationError
#         if hiv_test_review.participation_type_string == RBD and hiv_test_review.recorded_hiv_result != 'POS':
#             raise exception_cls('Please review Participation form. For a RBD only participation, \'positive\' HIV test result has to be chosen.')

    def get_test_code(self):
        return 'HIV'

    def get_result_datetime(self):
        return datetime(self.hiv_test_date.year, self.hiv_test_date.month, self.hiv_test_date.day)

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "HIV Test Review"
        verbose_name_plural = "HIV Test Review"

from django.db import models
from django.utils.translation import ugettext as _
from edc_base.audit_trail import AuditTrail
from edc.subject.locator.models import BaseLocator
from edc.choices.common import YES_NO
from edc.base.model.validators import BWCellNumber, BWTelephoneNumber
from edc.core.crypto_fields.fields import EncryptedCharField
from apps.bcpp_household.models  import Household
from apps.bcpp_subject.managers import ScheduledModelManager
from .subject_off_study_mixin import SubjectOffStudyMixin
from .htc_subject_visit import HtcSubjectVisit


class HtcSubjectLocator(SubjectOffStudyMixin, BaseLocator):

    htc_subject_visit = models.ForeignKey(HtcSubjectVisit, null=True)

    alt_contact_cell_number = EncryptedCharField(
        max_length=8,
        verbose_name=_("Cell number (alternate)"),
        validators=[BWCellNumber, ],
        help_text="",
        blank=True,
        null=True,
        )
    has_alt_contact = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name=_("If we are unable to contact the person indicated above, is there another"
                      " individual (including next of kin) with whom the study team can get"
                      " in contact with?"),
        help_text="",
        )

    alt_contact_name = EncryptedCharField(
        max_length=35,
        verbose_name=_("Full Name of the responsible person"),
        help_text="include first name and surname",
        blank=True,
        null=True,
        )

    alt_contact_rel = EncryptedCharField(
        max_length=35,
        verbose_name=_("Relationship to participant"),
        blank=True,
        null=True,
        help_text="",
        )
    alt_contact_cell = EncryptedCharField(
        max_length=8,
        verbose_name=_("Cell number"),
        validators=[BWCellNumber, ],
        help_text="",
        blank=True,
        null=True,
        )

    other_alt_contact_cell = EncryptedCharField(
        max_length=8,
        verbose_name=_("Cell number (alternate)"),
        validators=[BWCellNumber, ],
        help_text="",
        blank=True,
        null=True,
        )

    alt_contact_tel = EncryptedCharField(
        max_length=8,
        verbose_name=_("Telephone number"),
        validators=[BWTelephoneNumber, ],
        help_text="",
        blank=True,
        null=True,
        )

    history = AuditTrail()

    objects = ScheduledModelManager()

    def dispatch_container_lookup(self, using=None):
        return (Household, 'htc_subject_visit__household_member__household_structure__household__household_identifier')

    def save(self, *args, **kwargs):
        # as long as locator is on a visit schedule, need to update self.registered_subject manually
        if self.subject_visit:
            if not self.registered_subject:
                self.registered_subject = self.registered_subject = self.subject_visit.appointment.registered_subject
        super(HtcSubjectLocator, self).save(*args, **kwargs)

    def natural_key(self):
        return self.subject_visit.natural_key()

    def get_visit(self):
        return self.subject_visit

    def get_subject_identifier(self):
        if self.get_visit():
            return self.get_visit().get_subject_identifier()
        return None

    def get_report_datetime(self):
        return self.created

    def __unicode__(self):
        return unicode(self.subject_visit)

    class Meta:
        verbose_name = 'HTC Subject Locator'
        app_label = 'bcpp_htc_subject'

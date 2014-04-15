from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import BWCellNumber, BWTelephoneNumber
from edc.choices.common import YES_NO
from edc.core.crypto_fields.fields import EncryptedCharField
from edc.entry_meta_data.managers import EntryMetaDataManager
from edc.export.managers import ExportHistoryManager
from edc.export.models import ExportTrackingFieldsMixin
from edc.subject.locator.models import BaseLocator

from apps.bcpp_household.models  import Plot

from ..managers import ScheduledModelManager


from .subject_off_study_mixin import SubjectOffStudyMixin
from .subject_visit import SubjectVisit


class SubjectLocator(ExportTrackingFieldsMixin, SubjectOffStudyMixin, BaseLocator):

    subject_visit = models.ForeignKey(SubjectVisit, null=True)

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

    export_history = ExportHistoryManager()

    entry_meta_data_manager = EntryMetaDataManager(SubjectVisit)

    history = AuditTrail()

    objects = ScheduledModelManager()

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'subject_visit__household_member__household_structure__household__plot__plot_identifier')

    def save(self, *args, **kwargs):
        self.hic_enrollment_checks()
        # as long as locator is on a visit schedule, need to update self.registered_subject manually
        if self.subject_visit:
            if not self.registered_subject:
                self.registered_subject = self.registered_subject = self.subject_visit.appointment.registered_subject
        super(SubjectLocator, self).save(*args, **kwargs)

    def hic_enrollment_checks(self, exception_cls=None):
        from .hic_enrollment import HicEnrollment
        exception_cls = exception_cls or ValidationError
        if HicEnrollment.objects.filter(subject_visit=self.subject_visit).exists():
            if not self.subject_cell and not self.subject_cell_alt and not self.subject_phone:
                raise exception_cls('An HicEnrollment form exists for this subject. At least one of \'subject_cell\', \'subject_cell_alt\' or \'subject_phone\' is required.')

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

    @property
    def ready_to_export_transaction(self):
        """Evaluates to True if the subject has a referral instance with a referral code to avoid exporting someone who is not being referred."""
        from .subject_referral import SubjectReferral
        try:
            return SubjectReferral.objects.get(subject_visit=self.subject_visit).referral_code
        except SubjectReferral.DoesNotExist:
            return False
        return None

    def __unicode__(self):
        return unicode(self.subject_visit)

    class Meta:
        verbose_name = 'Subject Locator'
        app_label = 'bcpp_subject'

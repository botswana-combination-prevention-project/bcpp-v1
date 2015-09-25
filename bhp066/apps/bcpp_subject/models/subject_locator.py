from django.db import models
from django.core.exceptions import ValidationError

from edc_base.audit_trail import AuditTrail
from edc_base.bw.validators import BWCellNumber, BWTelephoneNumber
from edc.choices.common import YES_NO, YES, NO
from edc_base.encrypted_fields import EncryptedCharField
from edc.entry_meta_data.managers import EntryMetaDataManager
from edc.export.managers import ExportHistoryManager
from edc.export.models import ExportTrackingFieldsMixin
from edc.subject.locator.models import BaseLocator
from edc.data_manager.models import TimePointStatusMixin
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.device.sync.models import BaseSyncUuidModel

from bhp066.apps.bcpp_household.models import Plot


from ..managers import SubjectLocatorManager

from .subject_off_study_mixin import SubjectOffStudyMixin
from .subject_visit import SubjectVisit
from .subject_consent import SubjectConsent


class SubjectLocator(ExportTrackingFieldsMixin, SubjectOffStudyMixin, BaseLocator, TimePointStatusMixin,
                     BaseDispatchSyncUuidModel, BaseSyncUuidModel):
    """A model completed by the user to that captures participant locator information
    and permission to contact."""

    CONSENT_MODEL = SubjectConsent

    subject_visit = models.ForeignKey(SubjectVisit, null=True)

    alt_contact_cell_number = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number (alternate)",
        validators=[BWCellNumber, ],
        help_text="",
        blank=True,
        null=True,
    )
    has_alt_contact = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="If we are unable to contact the person indicated above, is there another"
                     " individual (including next of kin) with whom the study team can get"
                     " in contact with?",
        help_text="",
    )

    alt_contact_name = EncryptedCharField(
        max_length=35,
        verbose_name="Full Name of the responsible person",
        help_text="include first name and surname",
        blank=True,
        null=True,
    )

    alt_contact_rel = EncryptedCharField(
        max_length=35,
        verbose_name="Relationship to participant",
        blank=True,
        null=True,
        help_text="",
    )
    alt_contact_cell = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number",
        validators=[BWCellNumber, ],
        help_text="",
        blank=True,
        null=True,
    )

    other_alt_contact_cell = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number (alternate)",
        validators=[BWCellNumber, ],
        help_text="",
        blank=True,
        null=True,
    )

    alt_contact_tel = EncryptedCharField(
        max_length=8,
        verbose_name="Telephone number",
        validators=[BWTelephoneNumber, ],
        help_text="",
        blank=True,
        null=True,
    )

    export_history = ExportHistoryManager()

    entry_meta_data_manager = EntryMetaDataManager(SubjectVisit)

    history = AuditTrail()

    objects = SubjectLocatorManager()

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
        if (self.may_follow_up == YES) or (self.may_follow_up == NO and self.may_sms_follow_up == YES):
            if not self.subject_cell and not self.subject_cell_alt and not self.subject_phone:
                try:
                    HicEnrollment.objects.get(
                        subject_visit__subject_idenifier=self.subject_visit.subject_identifier)
                    raise exception_cls(
                        'An HicEnrollment form exists for this subject. At least one of '
                        '\'subject_cell\', \'subject_cell_alt\' or \'subject_phone\' is required.')
                except HicEnrollment.DoesNotExist:
                    pass

    def natural_key(self):
        return self.subject_visit.natural_key()

    def get_visit(self):
        return self.subject_visit

    def get_subject_identifier(self):
        try:
            return self.get_visit().get_subject_identifier()
        except AttributeError:
            return self.registered_subject.subject_identifier

    @property
    def ready_to_export_transaction(self):
        """Evaluates to True only if the subject has a referral instance with a referral code
        to avoid exporting locator information on someone who is not yet been referred.

        ...see_also:: SubjectReferral."""
        try:
            SubjectReferral = models.get_model('bcpp_subject', 'subjectreferral')
            subject_referral = SubjectReferral.objects.get(subject_visit=self.subject_visit)
            if subject_referral.referral_code:
                return True
        except SubjectReferral.DoesNotExist:
            pass
        return False

    @property
    def formatted_locator_information(self):
        """Returns a formatted string that summarizes contact and locator info."""
        info = 'May not follow-up.'
        if self.may_follow_up == 'Yes':
            info = (
                '{may_sms_follow_up}\n'
                'Cell: {subject_cell} {alt_subject_cell}\n'
                'Phone: {subject_phone} {alt_subject_phone}\n'
                '').format(
                    may_sms_follow_up='SMS permitted' if self.may_sms_follow_up == 'Yes' else 'NO SMS!',
                    subject_cell='{} (primary)'.format(self.subject_cell) if self.subject_cell else '(none)',
                    alt_subject_cell=self.subject_cell_alt,
                    subject_phone=self.subject_phone or '(none)', alt_subject_phone=self.subject_phone_alt
            )
            if self.may_call_work == 'Yes':
                info = (
                    '{info}\n Work Contacts:\n'
                    '{subject_work_place}\n'
                    'Work Phone: {subject_work_phone}\n'
                    '').format(
                        info=info,
                        subject_work_place=self.subject_work_place or '(work place not known)',
                        subject_work_phone=self.subject_work_phone)
            if self.may_contact_someone == 'Yes':
                info = (
                    '{info}\n Contacts of someone else:\n'
                    '{contact_name} - {contact_rel}\n'
                    '{contact_cell} (cell), {contact_phone} (phone)\n'
                    '').format(
                        info=info,
                        contact_name=self.contact_name or '(name?)',
                        contact_rel=self.contact_rel or '(relation?)',
                        contact_cell=self.contact_cell or '(----)',
                        contact_phone=self.contact_phone or '(----)'
                )
            if info:
                info = ('{info}'
                        'Physical Address:\n{physical_address}').format(
                            info=info, physical_address=self.physical_address)
        return info

    def __unicode__(self):
        return unicode(self.subject_visit)

    class Meta:
        verbose_name = 'Subject Locator'
        app_label = 'bcpp_subject'

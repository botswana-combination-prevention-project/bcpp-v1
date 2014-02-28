from django.db import models
from django.utils.translation import ugettext as _

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import BWCellNumber, BWTelephoneNumber
from edc.choices.common import YES_NO
from edc.core.crypto_fields.fields import EncryptedCharField
from edc.entry_meta_data.managers import EntryMetaDataManager
from edc.subject.locator.models import BaseLocator

from apps.bcpp_household.models  import Plot

from apps.bcpp_subject.managers import ScheduledModelManager
from .subject_visit_rbd import SubjectVisitRBD
from apps.bcpp_subject.models import SubjectOffStudyMixin

class SubjectLocatorRBD(SubjectOffStudyMixin, BaseLocator):

    subject_visit_rbd = models.ForeignKey(SubjectVisitRBD, null=True)

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
        verbose_name=("If we are unable to contact the person indicated above, is there another"
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

    entry_meta_data_manager = EntryMetaDataManager(SubjectVisitRBD)

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'subject_visit_rbd__household_member__household_structure__household__plot__plot_identifier')

    def save(self, *args, **kwargs):
        # as long as locator is on a visit schedule, need to update self.registered_subject manually
        if self.subject_visit_rbd:
            if not self.registered_subject:
                self.registered_subject = self.registered_subject = self.subject_visit_rbd.appointment.registered_subject
        super(SubjectLocatorRBD, self).save(*args, **kwargs)

    def natural_key(self):
        return self.subject_visit_rbd.natural_key()

    def get_visit(self):
        return self.subject_visit_rbd

    def get_subject_identifier(self):
        if self.get_visit():
            return self.get_visit().get_subject_identifier()
        return None

    def get_report_datetime(self):
        return self.created

    def __unicode__(self):
        return unicode(self.subject_visit_rbd)

    class Meta:
        verbose_name = 'Research Blood Draw Subject Locator'
        app_label = 'bcpp_rbd_subject'

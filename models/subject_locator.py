from django.db import models
from audit_trail.audit import AuditTrail
from bhp_locator.models import BaseLocator
from bhp_common.choices import YES_NO
from bhp_base_model.validators import BWCellNumber, BWTelephoneNumber
from bhp_crypto.fields import EncryptedCharField
from bcpp_subject.models import SubjectVisit


class SubjectLocator(BaseLocator):

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
        verbose_name=("If we are unable to contact the person indicated above, is there another"
                      " individual (including next of kin) with whom the study team can get"
                      " in contact with?"),
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

    history = AuditTrail(show_in_admin=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        # as long as locator is on a visit schedule, need to update self.registered_subject manually
        if self.subject_visit:
            if not self.registered_subject:
                self.registered_subject = self.registered_subject = self.subject_visit.appointment.registered_subject
        super(SubjectLocator, self).save(*args, **kwargs)

    def get_visit(self):
        return self.subject_visit

    def get_subject_identifier(self):
        return self.get_visit().get_subject_identifier()

    def get_report_datetime(self):
        return self.created

    def __unicode__(self):
        return unicode(self.subject_visit)

    class Meta:
        verbose_name = 'Subject Locator'
        app_label = 'cancer_subject'

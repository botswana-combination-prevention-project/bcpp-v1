from datetime import date, datetime
from django.db import models
from bhp_consent.models import BaseConsentedUuidModel
from bhp_base_model.validators import datetime_not_before_study_start, datetime_not_future
from bhp_common.choices import YES_NO, YES_NO_DOESNT_WORK
from bhp_base_model.validators import BWCellNumber, BWTelephoneNumber
from bhp_crypto.fields import EncryptedCharField, EncryptedTextField
from bhp_registration.models import RegisteredSubject
from bhp_locator.managers import BaseLocatorManager


class BaseLocator(BaseConsentedUuidModel):

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    report_datetime = models.DateTimeField("Today's date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.today(),
        )
    date_signed = models.DateField(
        verbose_name="1. Date Locator Form signed ",
        default=date.today(),
        help_text="",
        )
    mail_address = EncryptedTextField(
        max_length=500,
        verbose_name="Mailing address ",
        help_text="",
        null=True,
        blank=True
        )
    home_visit_permission = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Has the participant given her permission for study staff to make home visits for follow-up purposes before and during the study?",
        )
    physical_address = EncryptedTextField(
        max_length=500,
        verbose_name="Physical address with detailed description",
        blank=True,
        null=True,
        help_text="",
        )
    may_follow_up = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="3. Has the participant given her permission for study staff to call her for follow-up purposes before and during the study?",
        )
    subject_cell = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number",
        validators=[BWCellNumber, ],
        blank=True,
        null=True,
        help_text="",
        )
    subject_cell_alt = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number (alternate)",
        validators=[BWCellNumber, ],
        help_text="",
        blank=True,
        null=True,
        )
    subject_phone = EncryptedCharField(
        max_length=8,
        verbose_name="Telephone",
        validators=[BWTelephoneNumber, ],
        help_text="",
        blank=True,
        null=True,
        )
    subject_phone_alt = EncryptedCharField(
        max_length=8,
        verbose_name="Telephone (alternate)",
        help_text="",
        validators=[BWTelephoneNumber, ],
        blank=True,
        null=True,
        )
    may_call_work = models.CharField(
        max_length=25,
        choices=YES_NO_DOESNT_WORK,
        verbose_name="Has the participant given her permission for study staff to contact her at work for follow up purposes before and during the study?",
        help_text=" if 'No' go to section B, otherwise continue"
        )
    subject_work_place = EncryptedTextField(
        max_length=500,
        verbose_name="Name and location of work place",
        help_text="",
        blank=True,
        null=True,
        )
    subject_work_phone = EncryptedCharField(
        max_length=8,
        verbose_name="Work telephone number ",
        help_text="",
        validators=[BWTelephoneNumber, ],
        blank=True,
        null=True,
        )
    may_contact_someone = models.CharField(
        max_length=25,
        choices=YES_NO,
        verbose_name="Has the participant given her permission for study staff to contact anyone else for follow-up purposes before and during the study?",
        help_text="For example a partner, spouse, family member, neighbour ...",
        )
    contact_name = EncryptedCharField(
        max_length=35,
        verbose_name="Full names of the contact person",
        blank=True,
        null=True,
        help_text="",
        )
    contact_rel = EncryptedCharField(
        max_length=35,
        verbose_name="Relationship to participant",
        blank=True,
        null=True,
        help_text="",
        )
    contact_physical_address = EncryptedTextField(
        max_length=500,
        verbose_name="Full physical address ",
        blank=True,
        null=True,
        help_text="",
        )
    contact_cell = EncryptedCharField(
        max_length=8,
        verbose_name="Cell number",
        validators=[BWCellNumber, ],
        help_text="",
        blank=True,
        null=True,
        )
    contact_phone = EncryptedCharField(
        max_length=8,
        verbose_name="Telephone number",
        validators=[BWTelephoneNumber, ],
        help_text="",
        blank=True,
        null=True,
        )

    objects = BaseLocatorManager()

    def natural_key(self):
        return (self.report_datetime, ) + self.registered_subject.natural_key()

    class Meta:
        abstract = True

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from bhp_common.choices import GENDER, ART_STATUS_UNKNOWN, POS_NEG_UNKNOWN
from bhp_base_model.classes import BaseUuidModel
from bhp_base_model.fields import InitialsField, IsDateEstimatedField
from bhp_base_model.validators import dob_not_future
from lab_account.models import Account
from lab_patient.managers import PatientManager


class Patient(BaseUuidModel):

    subject_identifier = models.CharField('Subject Identifier',
        max_length=25,
        unique=True,
        help_text='',
        db_index=True,
        )

    account = models.ManyToManyField(Account,
        null=True,
        blank=True,
        )

    initials = InitialsField()

    gender = models.CharField(
        verbose_name=_("Gender"),
        max_length=3,
        choices=GENDER,
        )

    dob = models.DateField(
        verbose_name=_("Date of birth"),
        validators=[
            dob_not_future,
            ],
        help_text=_("Format is YYYY-MM-DD"),
        )

    is_dob_estimated = IsDateEstimatedField(
        verbose_name=_("Is the subject's date of birth estimated?"),
    )

    hiv_status = models.CharField(
        max_length=10,
        choices=POS_NEG_UNKNOWN,
        default='UNKNOWN',
        )

    art_status = models.CharField(
        max_length=10,
        choices=ART_STATUS_UNKNOWN,
        default='UNKNOWN',
        )

    comment = models.CharField("Comment",
        max_length=250,
        blank=True
        )

    objects = PatientManager()

    def get_absolute_url(self):
        return reverse('admin:lab_patient_patient_change', args=(self.id,))

    def __unicode__(self):
        return "%s" % (self.subject_identifier)

    class Meta:
        ordering = ["subject_identifier"]
        unique_together = ['subject_identifier', ]
        app_label = 'lab_patient'
        db_table = 'bhp_lab_registration_patient'

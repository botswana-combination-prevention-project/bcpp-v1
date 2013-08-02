from django.db import models
from audit_trail.audit import AuditTrail
from bhp_common.choices import GENDER
from bhp_base_model.fields import OtherCharField
from bhp_crypto.fields import EncryptedCharField, EncryptedDecimalField
from bcpp.choices import YES_NO
from bcpp_subject.choices import RELATION
from base_scheduled_visit_model import BaseScheduledVisitModel
from bhp_dispatch.models import BaseDispatchSyncUuidModel


class HouseholdComposition (BaseScheduledVisitModel):

    physical_add = EncryptedCharField(
        verbose_name="Description of physical address: ",
        max_length=150,
        blank=True,
        null=True,
        help_text="",
        )

    coordinates = EncryptedDecimalField(
        verbose_name="GPS coordinates",
        max_digits=10,
        decimal_places=4,
        help_text=" Record coordinates of the main gate to the household",
        )

    contact = models.CharField(
        verbose_name="[To the respondent] Can we contact you by telephone?",
        max_length=3,
        choices=YES_NO,
        help_text="",
        )

    phone_number = models.IntegerField(
        verbose_name="[To the respondent] What phone numbers can we use to reach you?",
        max_length=25,
        help_text="",
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Household Composition"
        verbose_name_plural = "Household Composition"


class Respondent (BaseDispatchSyncUuidModel):

    household_composition = models.ForeignKey(HouseholdComposition)

    first_name = EncryptedCharField(
        verbose_name="First name or initials ",
        max_length=25,
        )
    relation = models.CharField(
        verbose_name="Relation",
        choices=RELATION,
        max_length=25,
        )
    relation_other = OtherCharField()

    gender = models.CharField(
        verbose_name="Gender",
        max_length=6,
        choices=GENDER,
        )
    age = models.IntegerField(
        verbose_name="Age",
        max_length=2,
        )
    present = models.CharField(
        verbose_name="Present Today",
        max_length=3,
        choices=YES_NO,
        )
    nights_outside = models.IntegerField(
        verbose_name="Nights Outside Community",
        max_length=2,
        )

    history = AuditTrail()

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Respondent Details"
        verbose_name_plural = "Respondent Details"

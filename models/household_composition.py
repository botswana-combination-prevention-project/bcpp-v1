from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bhp_common.choices import YES_NO, GENDER
from bhp_base_model.fields import OtherCharField
from bhp_crypto.fields import EncryptedCharField, EncryptedDecimalField
from bcpp_subject.choices import RELATION
from base_scheduled_visit_model import BaseScheduledVisitModel
from my_base_uuid_model import MyBaseUuidModel


class HouseholdComposition (BaseScheduledVisitModel):
    
    """CS004"""
    
    """Instructions To be completed by a household member at least 18 years of age"
    " who has heard the consent script about these questions and is willing to answer. """
    
    housecode = EncryptedCharField(
        verbose_name="1. Household code",
        max_length=25,
        blank=True,
        null=True,
        help_text="",
        )
    
    physical_add = EncryptedCharField(
        verbose_name="2. Description of physical address: ",
        max_length=150,
        blank=True,
        null=True,
        help_text="",
        )

    coordinates = EncryptedDecimalField(
        verbose_name = "3. GPS coordinates",
        max_digits=10,
        decimal_places=4,
        help_text=" Record coordinates of the main gate to the household",
        )

    contact = models.CharField(
        verbose_name = "4. [To the respondent] Can we contact you by telephone?",
        max_length = 3,
        choices = YES_NO,
        help_text="",
        )

    phone_number = models.IntegerField(
        verbose_name = "5. [To the respondent] What phone numbers can we use to reach you?",
        max_length = 25,
        help_text="",
        )
    
    history = AuditTrail()

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_householdcomposition_change', args=(self.id,))

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Household Composition"
        verbose_name_plural = "Household Composition"


class Details (MyBaseUuidModel):
     
    first_name = models.CharField(
        verbose_name="First name or initials ",
        max_length=25,
        blank=True,
        null=True,
        help_text="",
        )
    relation = models.CharField(
        verbose_name="Relation",
        choices=RELATION,
        max_length=25,
        blank=True,
        null=True,
        help_text="",
        )
    relation_other = OtherCharField()
    
    gender = models.CharField(
        verbose_name="Gender",
        max_length=6,
        choices=GENDER,
        blank=True,
        null=True,
        help_text="",
        )
    age = models.IntegerField(
        verbose_name="Age",
        max_length=2,
        blank=True,
        null=True,
        help_text="",
        )
    present = models.CharField(
        verbose_name="Present Today",
        max_length=3,
        choices=YES_NO,
        blank=True,
        null=True,
        help_text="",
        )
    nights_outside = models.IntegerField(
        verbose_name="Nights Outside Community",
        max_length=2,
        blank=True,
        null=True,
        help_text="",
        )
    class Meta:
        abstract = True


class Respondent (Details):
    
    household_composition= models.ForeignKey(HouseholdComposition)
    
    history = AuditTrail()
    
    class Meta: 
        app_label = 'bcpp_subject'
        verbose_name = "Respondent Details"
        verbose_name_plural = "Respondent Details"
    
from django.db import models
from bcpp_household.models import Household
from bhp_crypto.fields import EncryptedTextField
from bhp_dispatch.models import BaseDispatchSyncUuidModel


class HouseholdDescription(BaseDispatchSyncUuidModel):
    
    household = models.ForeignKey(Household, null=True, editable=False)
    
    eligible_members = models.IntegerField(
        verbose_name="Number of Eligible member",
        blank=True,
        null=True,
        help_text=("Provide the number of people who live in the household who are eligible."),)
    
    description = EncryptedTextField(
        verbose_name="House household description",
        max_length=250,
        help_text=("You may provide a comment here about the house description, e.g color of the house."),
        blank=True,
        null=True,
        )
    
    num_household = models.IntegerField(
        verbose_name="Number of Households in a plot.",
        blank=True,
        null=True,
        help_text=("Provide the number of Households in a plot.."),)
    
    comment = EncryptedTextField(
        max_length=250,
        help_text=("You may provide a comment here or leave BLANK."),
        blank=True,
        null=True,
        )
    
    availability_datetime = models.DateTimeField(
        verbose_name='General Date/Time when most of the household members will be available',
        null=True,
        )
    
    class Meta:
        app_label = 'bcpp_household'
        verbose_name = 'Household Description (CLO)'
        verbose_name_plural = 'Household Description (CLO)'

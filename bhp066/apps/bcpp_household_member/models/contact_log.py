from django.db import models
from django.core.urlresolvers import reverse

from edc.choices.common import YES_NO
from edc.device.dispatch.models import BaseDispatchSyncUuidModel

from bhp066.apps.bcpp_household.choices import INFO_PROVIDER, STATUS

from ..managers import ContactLogManager, ContactLogItemManager


class ContactLog(BaseDispatchSyncUuidModel):
    """Not used"""
    objects = ContactLogManager()

    def natural_key(self):
        return (self.id)

    def get_absolute_url(self):
        return reverse('admin:bcpp_household_contactlog_change', args=(self.id, ))

    class Meta:
        app_label = 'bcpp_household_member'


class ContactLogItem(BaseDispatchSyncUuidModel):
    """Not used"""
    contact_log = models.ForeignKey(ContactLog)

    contact_datetime = models.DateTimeField()

    subject_status = models.CharField(
        verbose_name='Subject Status',
        max_length=10,
        choices=STATUS)

    is_contacted = models.CharField(
        verbose_name='Contacted?',
        max_length=10,
        choices=YES_NO)

    information_provider = models.CharField(
        choices=INFO_PROVIDER,
        max_length=20,
        help_text="",
        null=True,
        blank=True,
    )

    appointment_datetime = models.DateTimeField(
        verbose_name='Appointment',
        null=True, blank=True)

    try_again = models.CharField(
        verbose_name="Try to contact again?",
        max_length=10,
        choices=YES_NO)

    comment = models.TextField(
        max_length=50,
        blank=True,
        null=True,
    )

    objects = ContactLogItemManager()

    def natural_key(self):
        return (self.contact_datetime, ) + self.contact_log.natural_key()

    class Meta:
        app_label = 'bcpp_household_member'

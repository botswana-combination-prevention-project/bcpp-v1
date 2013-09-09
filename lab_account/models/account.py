from django.db import models
from bhp_base_model.models import BaseUuidModel
from lab_account.models import AccountHolder

class Account (BaseUuidModel):

    account_name = models.CharField(
        max_length=25,
        unique=True,
        )

    account_opendate = models.DateField(
        verbose_name='Open date',
        )

    account_closedate = models.DateField(
        verbose_name='Closed date',
        )

    account_holder = models.ForeignKey(AccountHolder,
        null=True,
        blank=True,
        )

    comment = models.CharField("Comment",
        max_length=250,
        blank=True,
        )

    objects = models.Manager()

    def get_absolute_url(self):
        return "/lab_account/account/%s/" % self.id

    def __unicode__(self):
        return self.account_name

    class Meta:
        ordering = ["account_name"]
        app_label = 'lab_account'
        db_table = 'bhp_lab_registration_account'

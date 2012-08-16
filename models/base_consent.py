#from django.db import models
from django.utils.translation import ugettext_lazy as _
from bhp_base_model.fields import IdentityTypeField
from bhp_botswana.fields import EncryptedOmangField
from bhp_consent.classes import BaseConsent as BaseBaseConsent


class BaseConsent(BaseBaseConsent):

    """ because of the identity field, this is a Botswana model """

    identity = EncryptedOmangField(
        verbose_name=_("Identity number (OMANG, etc)"),
        unique=True,
        help_text=_("Use Omang, Passport number, driver's license number or Omang receipt number")
        )

    identity_type = IdentityTypeField()

    class Meta:
        abstract = True

#from django.db import models
from django.utils.translation import ugettext_lazy as _
from bhp_base_model.fields import IdentityTypeField
from bhp_botswana.fields import EncryptedOmangField
from bhp_consent.models import BaseConsent


class BaseBwConsent(BaseConsent):

    """ because of the identity field, this is a Botswana model """

    identity = EncryptedOmangField(
        verbose_name=_("Identity number (OMANG, etc)"),
        unique=True,
        help_text=_("Use Omang, Passport number, driver's license number or Omang receipt number")
        )

    identity_type = IdentityTypeField()

    confirm_identity = EncryptedOmangField(
        help_text="Retype the identity number from the identity card",
        null=True,
        blank=False)

    class Meta:
        abstract = True

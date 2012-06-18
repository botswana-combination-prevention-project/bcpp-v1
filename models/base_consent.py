#from django.db import models
from django.utils.translation import ugettext_lazy as _
from bhp_base_model.fields import IdentityTypeField
from bhp_botswana.fields import EncryptedOmangField
from bhp_consent.classes import BaseConsent


class BaseConsent(BaseConsent):
    
    """ because of the identity field, this is a Botswana model """

    identity = EncryptedOmangField(
        verbose_name = _("Identity number (OMANG, etc)"), 
        max_length = 512, 
        unique = True,
        help_text = _("Use Omang, Passport number, driver's license number or Omang receipt number")
        )

    identity_type = IdentityTypeField()

    class Meta:
        abstract = True


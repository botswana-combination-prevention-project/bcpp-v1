from bhp_base_model.fields import IdentityTypeField
from bhp_crypto.fields import EncryptedIdentityField
from bhp_consent.classes import BaseConsent


class Consent(BaseConsent):

    """ Standard consent model, may prefer to use the local model, e.g bhp_botswana.classes.base_consent """

    identity = EncryptedIdentityField(
        unique=True,
        null=True,
        blank=True,
        )

    identity_type = IdentityTypeField()

    def __unicode__(self):
        return unicode(self.subject_identifier)

    class Meta:
        abstract = True

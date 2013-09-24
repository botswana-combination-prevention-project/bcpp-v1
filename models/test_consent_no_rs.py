from django.db import models
from bhp_base_model.fields import IdentityTypeField
from bhp_crypto.fields import EncryptedIdentityField
from bhp_consent.models import BaseConsent
from bhp_consent.managers import BaseConsentManager


class TestConsentNoRs(BaseConsent):

    user_provided_subject_identifier = models.CharField(max_length=35, null=True)

    identity = EncryptedIdentityField(
        unique=True,
        null=True,
        blank=True,
        )

    identity_type = IdentityTypeField()

    confirm_identity = EncryptedIdentityField(
        unique=True,
        null=True,
        blank=True,
        )

    objects = BaseConsentManager()

    def is_dispatchable_model(self):
        return False

    def get_user_provided_subject_identifier_attrname(self):
        """Returns the attribute name of the user provided subject_identifier."""
        return 'user_provided_subject_identifier'

    def get_subject_type(self):
        return 'subject'

    class Meta:
        app_label = 'bhp_base_test'

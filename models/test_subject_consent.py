from django.db import models
from bhp_base_model.fields import IdentityTypeField
from bhp_crypto.fields import EncryptedIdentityField
from bhp_registration.models import RegisteredSubject
from bhp_consent.models import BaseConsent


class TestSubjectConsent(BaseConsent):

    """ Standard consent model.

    .. seealso:: :class:`BaseConsent` in :mod:`bhp_botswana.classes` """

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

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

    objects = models.Manager()

    def get_user_provided_subject_identifier_attrname(self):
        """Returns the attribute name of the user provided subject_identifier."""
        return 'user_provided_subject_identifier'

    def get_subject_type(self):
        return 'subject'

    def __unicode__(self):
        return unicode(self.subject_identifier)

    class Meta:
        app_label = 'bhp_consent'

from django.db import models
from bhp_base_model.fields import IdentityTypeField
from bhp_crypto.fields import EncryptedIdentityField
from bhp_consent.models import BaseConsent
from bhp_consent.exceptions import ConsentError


class TestSubjectConsent(BaseConsent):

    """ Standard consent model.

    .. seealso:: :class:`BaseConsent` in :mod:`bhp_botswana.classes` """

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

    def save(self, *args, **kwargs):
        if self.id:
            if self.get_user_provided_subject_identifier_attrname() in dir(self):
                if not self.subject_identifier == getattr(self, self.get_user_provided_subject_identifier_attrname()):
                    raise ConsentError('Field {0} cannot be changed.'.format(self.get_user_provided_subject_identifier_attrname()))
        super(TestSubjectConsent, self).save(*args, **kwargs)

    def get_user_provided_subject_identifier_attrname(self):
        """override to return the attribute name of the user provided subject_identifier."""
        return 'user_provided_subject_identifier'

    def get_subject_type(self):
        return 'subject'

    def __unicode__(self):
        return unicode(self.subject_identifier)

    class Meta:
        app_label = 'bhp_consent'

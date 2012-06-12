from django.db import models
from django.contrib.auth.models import User
from bhp_base_model.fields import InitialsField
from bhp_userprofile.choices import SALUTATION


class UserProfile(models.Model):
    # add AUTH_PROFILE_MODULE = "bhp_userprofile.bhpprofile" o settings.py
    # This is the only required field
    user = models.OneToOneField(User)

    salutation = models.CharField(
        max_length=10,
        choices=SALUTATION,
        default='NONE',
        )

    initials = InitialsField(
        unique=True,
        )

    def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    class Meta:
        app_label = 'bhp_userprofile'

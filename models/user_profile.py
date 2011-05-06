from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from bhp_common.fields import NameField, InitialsField

class UserProfile(models.Model):
    # add AUTH_PROFILE_MODULE = "bhp_userprofile.bhpprofile" o settings.py
    # This is the only required field
    user = models.OneToOneField(User)

    initials = InitialsField(
        unique=True,
        )

    def __unicode__(self):
        return '%s, %s' % (self.user.last_name, self.user.first_name)

    class Meta:
        app_label = 'bhp_userprofile'

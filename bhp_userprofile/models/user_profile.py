from django.db import models
from django.contrib.auth.models import User
from bhp_base_model.fields import InitialsField
from bhp_userprofile.choices import SALUTATION

#if not 'AUTH_PROFILE_MODULE' in dir(settings):
#    raise ImproperlyConfigured('Settings attribute AUTH_PROFILE_MODULE not found please add \'AUTH_PROFILE_MODULE = bhp_userprofile.UserProfile\' to your settings.py.')


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    salutation = models.CharField(
        max_length=10,
        choices=SALUTATION,
        default='NONE',)
    initials = InitialsField()
    # fields to control access to encryption keys
#    irreversible_rsa = models.BooleanField(
#        verbose_name='Allow access to irreversible keys',
#        default=False)
#    restricted_rsa = models.BooleanField(
#        verbose_name='Allow access to restricted RSA keys',
#        default=False)
#    local_rsa = models.BooleanField(
#        verbose_name='Allow access to local RSA keys',
#        default=False)
#    salter_rsa = models.BooleanField(
#        verbose_name='Allow access to salter RSA keys',
#        default=False)
#    local_aes = models.BooleanField(
#        verbose_name='Allow access to local AES keys',
#        default=False)

    def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    class Meta:
        app_label = 'bhp_userprofile'


#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#       UserProfile.objects.create(user=instance)
#
#post_save.connect(create_user_profile, sender=User)

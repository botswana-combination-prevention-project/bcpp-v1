
from django.db import models
from django.core.urlresolvers import reverse
#from django.core.urlresolvers import NoReverseMatch
from django_extensions.db.models import TimeStampedModel
from bhp_base_model.fields import HostnameCreationField, HostnameModificationField


class BaseModel(TimeStampedModel):

    """Base model class for all models. Adds created and modified values for user, date and hostname (computer). """

    user_created = models.CharField(max_length=250, verbose_name='user created', editable=False, default="", db_index=True)

    user_modified = models.CharField(max_length=250, verbose_name='user modified', editable=False, default="", db_index=True)

    hostname_created = HostnameCreationField(
         db_index=True)

    hostname_modified = HostnameModificationField(
        db_index=True)

    def get_absolute_url(self):
        if self.id:
            url = reverse('admin:{app_label}_{object_name}_change'.format(app_label=self._meta.app_label, object_name=self._meta.object_name.lower()), args=(self.id,))
        else:
            url = reverse('admin:{app_label}_{object_name}_add'.format(app_label=self._meta.app_label, object_name=self._meta.object_name.lower()))
        return url

    class Meta:
        abstract = True

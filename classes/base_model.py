from django.db import models
from django_extensions.db.models import TimeStampedModel
from bhp_base_model.fields import HostnameCreationField, HostnameModificationField


class BaseModel(TimeStampedModel):

    """Base model class for all models. Adds created and modified values for user, date and hostname (computer). """

    user_created = models.CharField(max_length=250, verbose_name='user created', editable=False, default="")

    user_modified = models.CharField(max_length=250, verbose_name='user modified', editable=False, default="")

    hostname_created = HostnameCreationField(
         db_index=True)

    hostname_modified = HostnameModificationField(
        db_index=True)

    class Meta:
        abstract = True

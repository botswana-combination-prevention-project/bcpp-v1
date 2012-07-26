from django.db import models
try:
    from bhp_sync.classes import BaseSyncModel as BaseUuidModel
except ImportError:
    from bhp_base_model.classes import BaseUuidModel


class Crypt (BaseUuidModel):

    """ A secrets lookup model searchable by hash """

    hash = models.CharField(
        verbose_name="Hash",
        max_length=128,
        db_index=True,
        unique=True,
        )

    secret = models.TextField(
        verbose_name="Secret",
        )

    algorithm = models.CharField(
        max_length=25,
        null=True)

    mode = models.CharField(
        max_length=25,
        null=True)

    salt = models.CharField(
        max_length=50,
        null=True)

    class Meta:
        app_label = 'bhp_crypto'
        verbose_name = 'Crypt'

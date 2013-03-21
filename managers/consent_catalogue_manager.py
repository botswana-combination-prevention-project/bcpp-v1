from django.db import models


class BaseConsentManager(models.Manager):

    def get_by_natural_key(self, name, version):
        return self.get(name=name, version=version)

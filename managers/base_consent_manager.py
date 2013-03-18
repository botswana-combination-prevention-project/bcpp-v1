from django.db import models


class BaseConsentManager(models.Manager):

    def get_by_natural_key(self, identity):
        return self.get(identity=identity)

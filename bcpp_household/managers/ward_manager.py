from django.db import models


class WardManager(models.Manager):

    def get_by_natural_key(self, ward_name, village_name):
        return self.get(ward_name=ward_name, village_name=village_name)

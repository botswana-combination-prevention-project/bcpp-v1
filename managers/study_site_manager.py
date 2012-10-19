from django.db import models


class StudySiteManager(models.Manager):

    def get_by_natural_key(self, site_code):
        return self.get(site_code=site_code,)

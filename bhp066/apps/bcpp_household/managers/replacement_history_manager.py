from django.db import models


class ReplacementHistoryManager(models.Manager):

    def get_by_natural_key(self, replacing_item, replaced_item):
        return self.get(replacing_item=replacing_item, replaced_item=replaced_item)

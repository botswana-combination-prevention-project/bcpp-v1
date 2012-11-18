from django.db import models


class AliquotConditionManager(models.Manager):

    def get_condition_ok(self):
        """Returns the instance for the "condition OK" record."""
        if self.filter(short_name='10'):
            aliquot_condition = self.get(short_name='10')
        else:
            raise TypeError('AliquotCondition must have at least one entry that has short_name=10 for condition is OK. Got None')
        return aliquot_condition

    def get_by_natural_key(self, name):
        return self.get(name=name)

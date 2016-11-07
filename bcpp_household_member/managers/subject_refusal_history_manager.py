from django.db import models

from bcpp.manager_mixins import CurrentCommunityManagerMixin


class SubjectRefusalHistoryManager(CurrentCommunityManagerMixin, models.Manager):

    lookup = ['subject_refusal', 'household_member', 'household_structure', 'household', 'plot']

    def get_by_natural_key(self, transaction):
        return self.get(transaction=transaction)

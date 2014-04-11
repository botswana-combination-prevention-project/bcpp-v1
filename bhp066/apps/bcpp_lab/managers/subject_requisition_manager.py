from django.db import models


class SubjectRequisitionManager(models.Manager):

    def get_by_natural_key(self, requisition_identifier):
        return self.get(requisition_identifier=requisition_identifier)

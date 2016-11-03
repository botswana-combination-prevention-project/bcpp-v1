from django.db import models


class SubjectRequisitionInspectorManager(models.Manager):

    def get_by_natural_key(self, subject_identifier, requisition_identifier):
        return self.get(subject_identifier=subject_identifier, requisition_identifier=requisition_identifier)

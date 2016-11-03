from edc.device.inspector.models import BaseInspector


class SubjectRequisitionInspector(BaseInspector):

    def natural_key(self):
        return (self.subject_identifier, self.requisition_identifier)

    class Meta:
        app_label = 'bcpp_inspector'
        verbose_name = 'Subject Requisition Inspector'

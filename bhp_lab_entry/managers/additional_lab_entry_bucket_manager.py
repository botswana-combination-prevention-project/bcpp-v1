from datetime import datetime
from django.db import models
from bhp_entry.managers import BaseEntryBucketManager
from bhp_lab_entry.models import LabEntryUnscheduled


class AdditionalLabEntryBucketManager(BaseEntryBucketManager):

    def get_by_natural_key(self, visit_definition_code, name, visit_instance, appt_status, visit_definition_code1, subject_identifier_as_pk):
        Appointment = models.get_model('bhp_appointment', 'Appointment')
        LabEntry = models.get_model('bhp_lab_entry', 'LabEntry')
        appointment = Appointment.objects.get_by_natural_key(visit_instance, appt_status, visit_definition_code1, subject_identifier_as_pk)
        lab_entry = LabEntry.objects.get_by_natural_key(visit_definition_code, name)
        return self.get(appointment=appointment, lab_entry=lab_entry)

    def get_labs_for(self, **kwargs):

        """Return a queryset of ScheduledLabEntryBucket objects for the given subject and appointment.

        Note that ScheduledLabEntryBucket objects are linked to a subject's appointment
        for visit_instance = '0'; that is, the first appointment for
        a timepoint/visit. """
        registered_subject = kwargs.get("registered_subject")
        if not registered_subject:
            raise TypeError("Manager get_lab_entries_for expected registered_subject. Got None.")
        appt_0 = kwargs.get("appointment")
        if appt_0:
            # get the scheduled crfs based on the appt for visit_instance = '0'
            additional_lab_entry_bucket = super(AdditionalLabEntryBucketManager, self).filter(
                                                registered_subject=registered_subject,
                                                appointment=appt_0).order_by('lab_entry_unscheduled__panel__name')
        else:
            additional_lab_entry_bucket = super(AdditionalLabEntryBucketManager, self).none()
        return additional_lab_entry_bucket

    def add_for(self, **kwargs):

        panel = kwargs.get('panel')
        visit_model_instance = kwargs.get('visit_model_instance')
        if 'appointment' not in [f.name for f in visit_model_instance._meta.fields if f.name == 'appointment']:
            raise AttributeError("AdditionalLabEntryBucketManager expects model %s to have attribute \'appointment\'." % visit_model_instance._meta.object_name)

        registered_subject = visit_model_instance.appointment.registered_subject
        lab_entry_unscheduled = LabEntryUnscheduled.objects.get(panel=panel)

        if not super(AdditionalLabEntryBucketManager, self).filter(
                registered_subject=registered_subject,
                appointment=visit_model_instance.appointment,
                lab_entry_unscheduled=lab_entry_unscheduled):
            # add to bucket
            super(AdditionalLabEntryBucketManager, self).create(
                registered_subject=registered_subject,
                appointment=visit_model_instance.appointment,
                lab_entry_unscheduled=lab_entry_unscheduled,
                fill_datetime=datetime.today(),
                due_datetime=datetime.today(),
                )

#     def update_status(self, **kwargs):
#
#         self.registered_subject = kwargs.get('registered_subject')
#         if not self.registered_subject:
#             raise AttributeError, 'AdditionalLabEntryBucketManager.update_status requires \'registered_subject\'. Got None'
#
#         requisition_model = kwargs.get('requisition_model')
#         action = kwargs.get('action', 'add_change')
#         comment = kwargs.get('comment', '----')
#         # get the requisition_instance
#         self.requisition_instance = requisition_model.objects.filter(qset)
#
#        if self.requisition_instance and self.registered_subject:
#
#             report_datetime = datetime.today()
#
#             if super(AdditionalLabEntryBucketManager, self).filter(registered_subject=self.registered_subject, lab_entry_unscheduled__panel=self.requisition_instance.panel):
#                 s = super(AdditionalLabEntryBucketManager, self).get(registered_subject=self.registered_subject, lab_entry_unscheduled__panel=self.requisition_instance.panel)
#                 status = self.get_status(
#                     action=action,
#                     report_datetime=report_datetime,
#                     entry_status=s.entry_status,
#                     entry_comment=comment
#                     )
#                 s.report_datetime = status['report_datetime']
#                 s.entry_status = status['entry_status']
#                 s.entry_comment = status['entry_comment']
#                 # clear close_datetime
#                 s.close_datetime = status['close_datetime']
#                 s.modified = datetime.today()
#                 # save
#                 s.save()
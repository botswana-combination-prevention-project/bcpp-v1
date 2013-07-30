from django.db.models import signals
from bhp_base_model.models import BaseModel
from bhp_sync.models.signals import serialize_on_save, serialize_m2m_on_save
from bhp_visit_tracking.models.signals import base_visit_tracking_add_or_update_entry_buckets_on_post_save #  , base_visit_tracking_on_post_save
from bhp_lab_tracker.models.signals import tracker_on_post_save, tracker_on_post_delete
from bhp_consent.models.signals import is_consented_instance_on_pre_save
from bhp_subject.models.signals import base_subject_get_or_create_registered_subject_on_post_save
from bhp_appointment.models import pre_appointment_contact_on_post_save, pre_appointment_contact_on_post_delete
from bhp_appointment_helper.models import prepare_appointments_on_post_save


class SignalManager(object):

    def __init__(self):
        self.audit_signals = []
        # populate a reference variable -- not used anywhere but should include all non-audit signals
        # that are referred to in disconnect/connect
        self.signal_register = [
            'serialize_m2m_on_save',
            'serialize_on_save',
            'tracker_on_post_save',
            'base_visit_tracking_add_or_update_entry_buckets_on_post_save',
            'base_visit_tracking_check_in_progress_on_post_save',
            'base_subject_get_or_create_registered_subject_on_post_save',
            'is_consented_instance_on_pre_save',
            'prepare_appointments_on_post_save',
            'pre_appointment_contact_on_post_save',
            'pre_appointment_contact_on_post_delete'
            ]
        self.signal_register.sort()

    def disconnect(self, obj):
        signals.m2m_changed.disconnect(serialize_m2m_on_save, weak=False, dispatch_uid="serialize_m2m_on_save")
        signals.post_save.disconnect(serialize_on_save, weak=False, dispatch_uid="serialize_on_save")
        signals.post_save.disconnect(tracker_on_post_save, weak=False, dispatch_uid="tracker_on_post_save")
        signals.post_delete.disconnect(tracker_on_post_delete, weak=False, dispatch_uid="tracker_on_post_delete")
        signals.post_save.disconnect(base_visit_tracking_add_or_update_entry_buckets_on_post_save, weak=False, dispatch_uid="base_visit_tracking_add_or_update_entry_buckets_on_post_save")
        #signals.post_save.disconnect(base_visit_tracking_on_post_save, weak=False, dispatch_uid="base_visit_tracking_check_in_progress_on_post_save")
        signals.pre_save.disconnect(base_subject_get_or_create_registered_subject_on_post_save, weak=False, dispatch_uid="base_subject_get_or_create_registered_subject_on_post_save")
        signals.pre_save.disconnect(is_consented_instance_on_pre_save, weak=False, dispatch_uid="is_consented_instance_on_pre_save")
        signals.post_save.disconnect(pre_appointment_contact_on_post_delete, weak=False, dispatch_uid="pre_appointment_contact_on_post_delete")
        signals.post_save.disconnect(pre_appointment_contact_on_post_save, weak=False, dispatch_uid="pre_appointment_contact_on_post_save")
        signals.post_save.disconnect(prepare_appointments_on_post_save, weak=False, dispatch_uid="prepare_appointments_on_post_save")
        self.disconnect_audit_trail_signals(obj)

    def reconnect(self):
        signals.post_save.connect(prepare_appointments_on_post_save, weak=False, dispatch_uid="prepare_appointments_on_post_save")
        signals.post_save.connect(pre_appointment_contact_on_post_save, weak=False, dispatch_uid="pre_appointment_contact_on_post_save")
        signals.post_save.connect(pre_appointment_contact_on_post_delete, weak=False, dispatch_uid="pre_appointment_contact_on_post_delete")
        signals.pre_save.connect(is_consented_instance_on_pre_save, weak=False, dispatch_uid="is_consented_instance_on_pre_save")
        signals.pre_save.connect(base_subject_get_or_create_registered_subject_on_post_save, weak=False, dispatch_uid="base_subject_get_or_create_registered_subject_on_post_save")
        #signals.post_save.connect(base_visit_tracking_on_post_save, weak=False, dispatch_uid="base_visit_tracking_check_in_progress_on_post_save")
        signals.post_save.connect(base_visit_tracking_add_or_update_entry_buckets_on_post_save, weak=False, dispatch_uid="base_visit_tracking_add_or_update_entry_buckets_on_post_save")
        signals.post_save.connect(tracker_on_post_save, weak=False, dispatch_uid="tracker_on_post_save")
        signals.post_delete.connect(tracker_on_post_delete, weak=False, dispatch_uid="tracker_on_post_delete")
        signals.post_save.connect(serialize_on_save, weak=False, dispatch_uid="serialize_on_save")
        signals.m2m_changed.connect(serialize_m2m_on_save, weak=False, dispatch_uid="serialize_m2m_on_save")
        self.reconnect_audit_trail_signals()

    def disconnect_audit_trail_signals(self, obj):
        self.set_audit_trail_signals_for_model(obj)
        for audit_signal in self.audit_signals:
            if audit_signal in signals.post_save.receivers:
                signals.post_save.receivers.remove(audit_signal)

    def reconnect_audit_trail_signals(self):
        for audit_signal in self.audit_signals:
            signals.post_save.receivers.append(audit_signal)
        self.audit_signals = []

    def get_signal_by_dispatch_uid(self, dispatch_uid):
        signal = None
        for receiver_signal in signals.post_save.receivers + signals.pre_delete.receivers:
            if str(receiver_signal[0][0]) == dispatch_uid:
                signal = receiver_signal
                break
        return signal

    def set_audit_trail_signals_for_model(self, obj):
        if isinstance(obj, BaseModel):
            object_name = obj._meta.object_name.lower()
        elif isinstance(obj, basestring):
            object_name = obj
        else:
            object_name = obj._meta.object_name.lower()
            #raise TypeError('Expected a model class or a string of the name of the model class. Got {0}'.format(obj))
        for dispatch_uid in ['audit_serialize_on_save_{0}audit'.format(object_name), 'audit_on_save_{0}audit'.format(object_name), 'audit_delete_{0}audit'.format(object_name)]:
            audit_signal = self.get_signal_by_dispatch_uid(dispatch_uid)
            if audit_signal:
                self.audit_signals.append(audit_signal)

    def get_audit_trail_signals_for_model(self):
        if not self.audit_signals:
            raise AttributeError('Attribute \'audit_signals\' cannot be None. Call set first.')
        return self.audit_signals

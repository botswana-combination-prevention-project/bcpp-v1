from django.db.models import signals
from bhp_sync.classes import Consumer
from bcpp_household_member.models import base_household_member_consent_on_post_save, household_member_on_post_save, household_member_on_pre_save
from bcpp_household.models import household_structure_on_post_save, create_household_structure_on_post_save, check_for_survey_on_pre_save, \
                                   post_save_create_household
from bhp_subject.models import base_subject_get_or_create_registered_subject_on_post_save

class BcppConsumer(Consumer):

#    def __init__(self):
#        self.signal_manager = SignalManager()

    def disconnect_signals(self):
        """Disconnects signals before saving the serialized object in _to_json."""
#        self.signal_manager.disconnect()
        signals.post_save.disconnect(create_household_structure_on_post_save, weak=False, dispatch_uid="create_household_structure_on_post_save")
        signals.post_save.disconnect(household_structure_on_post_save, weak=False, dispatch_uid="household_structure_on_post_save")
        signals.post_save.disconnect(post_save_create_household, weak=False, dispatch_uid="post_save_create_household")
        signals.post_save.disconnect(base_household_member_consent_on_post_save, weak=False, dispatch_uid="base_household_member_consent_on_post_save")
        signals.post_save.disconnect(household_member_on_post_save, weak=False, dispatch_uid="household_member_on_post_save")
        signals.pre_save.disconnect(check_for_survey_on_pre_save, weak=False, dispatch_uid="check_for_survey_on_pre_save")
        signals.pre_save.disconnect(household_member_on_pre_save, weak=False, dispatch_uid="household_member_on_pre_save")
        signals.post_save.disconnect(base_subject_get_or_create_registered_subject_on_post_save, weak=False, dispatch_uid="base_subject_get_or_create_registered_subject_on_post_save")
        
    def reconnect_signals(self):
        """Reconnects signals after saving the serialized object in _to_json."""
#        self.signal_manager.reconnect()
        signals.post_save.connect(create_household_structure_on_post_save, weak=False, dispatch_uid="create_household_structure_on_post_save")
        signals.post_save.connect(household_structure_on_post_save, weak=False, dispatch_uid="household_structure_on_post_save")
        signals.post_save.connect(post_save_create_household, weak=False, dispatch_uid="post_save_create_household")
        signals.post_save.connect(base_household_member_consent_on_post_save, weak=False, dispatch_uid="base_household_member_consent_on_post_save")
        signals.post_save.connect(household_member_on_post_save, weak=False, dispatch_uid="household_member_on_post_save")
        signals.pre_save.connect(check_for_survey_on_pre_save, weak=False, dispatch_uid="check_for_survey_on_pre_save")
        signals.pre_save.connect(household_member_on_pre_save, weak=False, dispatch_uid="household_member_on_pre_save")
        signals.post_save.connect(base_subject_get_or_create_registered_subject_on_post_save, weak=False, dispatch_uid="base_subject_get_or_create_registered_subject_on_post_save")

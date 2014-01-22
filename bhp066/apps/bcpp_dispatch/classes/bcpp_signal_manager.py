from django.db.models import signals
from edc.device.sync.classes import Consumer
from edc.subject.subject.models import base_subject_get_or_create_registered_subject_on_post_save
from apps.bcpp_household_member.models import base_household_member_consent_on_post_save, household_member_on_post_save, household_member_on_pre_save, \
                                                absentee_visit_attempts_on_post_save, subject_absentee_entry_on_post_save
from apps.bcpp_household.models import (household_structure_on_post_save, post_save_on_household, check_for_survey_on_pre_save, create_household_on_post_save)
from apps.bcpp_subject.models import base_household_member_consent_on_post_save2


class BcppSignalManager(object):

    def _disconnect_bcpp_signals(self):
        """Disconnects signals before saving the serialized object in _to_json."""
        signals.pre_save.disconnect(household_member_on_pre_save, weak=False, dispatch_uid="household_member_on_pre_save")
        signals.post_save.disconnect(household_member_on_post_save, weak=False, dispatch_uid="household_member_on_post_save")
        signals.post_save.disconnect(base_household_member_consent_on_post_save, weak=False, dispatch_uid="base_household_member_consent_on_post_save")
        signals.post_save.disconnect(base_household_member_consent_on_post_save2, weak=False, dispatch_uid="base_household_member_consent_on_post_save2")
        signals.post_save.disconnect(create_household_on_post_save, weak=False, dispatch_uid="create_household_on_post_save")
        signals.post_save.disconnect(base_subject_get_or_create_registered_subject_on_post_save, weak=False, dispatch_uid="base_subject_get_or_create_registered_subject_on_post_save")
        signals.post_save.disconnect(post_save_on_household, weak=False, dispatch_uid="post_save_on_household")
        signals.post_save.disconnect(household_structure_on_post_save, weak=False, dispatch_uid="household_structure_on_post_save")
        signals.post_save.disconnect(subject_absentee_entry_on_post_save, weak=False, dispatch_uid="subject_absentee_entry_on_post_save")
        signals.post_save.disconnect(absentee_visit_attempts_on_post_save, weak=False, dispatch_uid="absentee_visit_attempts_on_post_save")
        signals.pre_save.disconnect(check_for_survey_on_pre_save, weak=False, dispatch_uid="check_for_survey_on_pre_save")

    def _reconnect_bcpp_signals(self):
        """Reconnects signals after saving the serialized object in _to_json."""
        signals.post_save.connect(household_member_on_post_save, weak=False, dispatch_uid="household_member_on_post_save")
        signals.pre_save.connect(household_member_on_pre_save, weak=False, dispatch_uid="household_member_on_pre_save")
        signals.post_save.connect(base_household_member_consent_on_post_save, weak=False, dispatch_uid="base_household_member_consent_on_post_save")
        signals.post_save.connect(base_household_member_consent_on_post_save2, weak=False, dispatch_uid="base_household_member_consent_on_post_save2")
        signals.post_save.connect(create_household_on_post_save, weak=False, dispatch_uid="create_household_on_post_save")
        signals.post_save.connect(base_subject_get_or_create_registered_subject_on_post_save, weak=False, dispatch_uid="base_subject_get_or_create_registered_subject_on_post_save")
        signals.post_save.connect(post_save_on_household, weak=False, dispatch_uid="post_save_on_household")
        signals.post_save.connect(household_structure_on_post_save, weak=False, dispatch_uid="household_structure_on_post_save")
        signals.post_save.connect(subject_absentee_entry_on_post_save, weak=False, dispatch_uid="subject_absentee_entry_on_post_save")
        signals.post_save.connect(absentee_visit_attempts_on_post_save, weak=False, dispatch_uid="absentee_visit_attempts_on_post_save")
        signals.pre_save.connect(check_for_survey_on_pre_save, weak=False, dispatch_uid="check_for_survey_on_pre_save")

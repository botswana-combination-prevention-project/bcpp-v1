from django.db.models import signals
from edc.device.sync.classes import Consumer
from edc.subject.subject.models import base_subject_get_or_create_registered_subject_on_post_save
from apps.bcpp_household_member.models import base_household_member_consent_on_post_save, household_member_on_post_save, household_member_on_pre_save
from apps.bcpp_household.models import (household_structure_on_post_save, post_save_on_household, check_for_survey_on_pre_save, create_household_on_post_save)
from .bcpp_signal_manager import BcppSignalManager


class BcppConsumer(Consumer, BcppSignalManager):

    def disconnect_signals(self):
        """Disconnects signals before saving the serialized object in _to_json."""
        self._disconnect_bcpp_signals()

    def reconnect_signals(self):
        """Reconnects signals after saving the serialized object in _to_json."""
        self._reconnect_bcpp_signals()

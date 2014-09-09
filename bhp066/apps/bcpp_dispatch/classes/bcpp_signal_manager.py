from django.db.models import signals
# from edc.subject.subject.models import base_subject_get_or_create_registered_subject_on_post_save
from apps.bcpp_household_member.models import (base_household_member_consent_on_post_save, enrollment_checklist_on_post_delete,
                                               household_member_on_post_save, household_member_on_pre_save, subject_xxx_on_post_save,
                                               enrollment_checklist_on_post_save, subject_refusal_on_post_delete, subject_absentee_entry_on_post_save,
                                               subject_undecided_entry_on_post_save, subject_htc_on_post_save, household_head_eligibility_on_post_save)
from apps.bcpp_household.models import (household_structure_on_post_save, household_refusal_on_delete,
                                        household_on_post_save, household_log_entry_on_post_save,
                                        household_assessment_on_delete, household_refusal_on_post_save,
                                        plot_on_post_save, plot_log_entry_on_post_save)
from apps.bcpp_subject.models import (subject_consent_on_post_save, update_subject_referral_on_post_save)


class BcppSignalManager(object):

    def _disconnect_bcpp_signals(self):
        """Disconnects signals before saving the serialized object in _to_json."""
        signals.post_save.disconnect(subject_xxx_on_post_save, weak=False, dispatch_uid="subject_xxx_on_post_save")
        signals.post_save.disconnect(subject_absentee_entry_on_post_save, weak=False, dispatch_uid="subject_absentee_entry_on_post_save")
        signals.post_save.disconnect(subject_undecided_entry_on_post_save, weak=False, dispatch_uid="subject_undecided_entry_on_post_save")
        signals.post_save.disconnect(subject_htc_on_post_save, weak=False, dispatch_uid="subject_htc_on_post_save")
        signals.post_save.disconnect(household_head_eligibility_on_post_save, weak=False, dispatch_uid="household_head_eligibility_on_post_save")
        signals.pre_save.disconnect(household_member_on_pre_save, weak=False, dispatch_uid="household_member_on_pre_save")
        signals.post_save.disconnect(household_member_on_post_save, weak=False, dispatch_uid="household_member_on_post_save")
        signals.post_save.disconnect(base_household_member_consent_on_post_save, weak=False, dispatch_uid="base_household_member_consent_on_post_save")
        signals.post_save.disconnect(plot_on_post_save, weak=False, dispatch_uid="plot_on_post_save")
        signals.post_save.disconnect(household_refusal_on_post_save, weak=False, dispatch_uid="household_refusal_on_post_save")
#        signals.post_save.disconnect(base_subject_get_or_create_registered_subject_on_post_save, weak=False, dispatch_uid="base_subject_get_or_create_registered_subject_on_post_save")
        signals.post_save.disconnect(household_on_post_save, weak=False, dispatch_uid="household_on_post_save")
        signals.post_save.disconnect(household_structure_on_post_save, weak=False, dispatch_uid="household_structure_on_post_save")
        signals.post_save.disconnect(plot_log_entry_on_post_save, weak=False, dispatch_uid="plot_log_entry_on_post_save")
        signals.post_delete.disconnect(household_refusal_on_delete, weak=False, dispatch_uid="household_refusal_on_delete")
        signals.post_save.disconnect(household_log_entry_on_post_save, weak=False, dispatch_uid="household_log_entry_on_post_save")
        signals.post_delete.disconnect(household_assessment_on_delete, weak=False, dispatch_uid="household_assessment_on_delete")
        signals.post_delete.disconnect(subject_refusal_on_post_delete, weak=False, dispatch_uid="subject_refusal_on_post_delete")
        signals.post_delete.disconnect(enrollment_checklist_on_post_delete, weak=False, dispatch_uid="enrollment_checklist_on_post_delete")
        signals.post_delete.disconnect(enrollment_checklist_on_post_save, weak=False, dispatch_uid="enrollment_checklist_on_post_save")
        signals.post_save.disconnect(subject_consent_on_post_save, weak=False, dispatch_uid="subject_consent_on_post_save")
        signals.post_save.disconnect(update_subject_referral_on_post_save, weak=False, dispatch_uid="update_subject_referral_on_post_save")

    def _reconnect_bcpp_signals(self):
        """Reconnects signals after saving the serialized object in _to_json."""
        signals.post_save.connect(subject_xxx_on_post_save, weak=False, dispatch_uid="subject_xxx_on_post_save")
        signals.post_save.connect(subject_absentee_entry_on_post_save, weak=False, dispatch_uid="subject_absentee_entry_on_post_save")
        signals.post_save.connect(subject_undecided_entry_on_post_save, weak=False, dispatch_uid="subject_undecided_entry_on_post_save")
        signals.post_save.connect(subject_htc_on_post_save, weak=False, dispatch_uid="subject_htc_on_post_save")
        signals.post_save.connect(household_head_eligibility_on_post_save, weak=False, dispatch_uid="household_head_eligibility_on_post_save")
        signals.post_save.connect(household_member_on_post_save, weak=False, dispatch_uid="household_member_on_post_save")
        signals.pre_save.connect(household_member_on_pre_save, weak=False, dispatch_uid="household_member_on_pre_save")
        signals.post_save.connect(base_household_member_consent_on_post_save, weak=False, dispatch_uid="base_household_member_consent_on_post_save")
        signals.post_save.connect(plot_on_post_save, weak=False, dispatch_uid="plot_on_post_save")
        signals.post_save.connect(household_refusal_on_post_save, weak=False, dispatch_uid="household_refusal_on_post_save")
#        signals.post_save.connect(base_subject_get_or_create_registered_subject_on_post_save, weak=False, dispatch_uid="base_subject_get_or_create_registered_subject_on_post_save")
        signals.post_save.connect(household_on_post_save, weak=False, dispatch_uid="household_on_post_save")
        signals.post_save.connect(household_structure_on_post_save, weak=False, dispatch_uid="household_structure_on_post_save")
        signals.post_save.connect(plot_log_entry_on_post_save, weak=False, dispatch_uid="plot_log_entry_on_post_save")
        signals.post_delete.connect(household_refusal_on_delete, weak=False, dispatch_uid="household_refusal_on_delete")
        signals.post_save.connect(household_log_entry_on_post_save, weak=False, dispatch_uid="household_log_entry_on_post_save")
        signals.post_delete.connect(household_assessment_on_delete, weak=False, dispatch_uid="household_assessment_on_delete")
        signals.post_delete.connect(subject_refusal_on_post_delete, weak=False, dispatch_uid="subject_refusal_on_post_delete")
        signals.post_delete.connect(enrollment_checklist_on_post_save, weak=False, dispatch_uid="enrollment_checklist_on_post_save")
        signals.post_delete.connect(enrollment_checklist_on_post_delete, weak=False, dispatch_uid="enrollment_checklist_on_post_delete")
        signals.post_save.connect(subject_consent_on_post_save, weak=False, dispatch_uid="subject_consent_on_post_save")
        signals.post_save.connect(update_subject_referral_on_post_save, weak=False, dispatch_uid="update_subject_referral_on_post_save")

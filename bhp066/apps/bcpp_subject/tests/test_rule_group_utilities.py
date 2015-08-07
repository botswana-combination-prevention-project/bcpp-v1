from edc.constants import NEW, NOT_REQUIRED, KEYED, REQUIRED, POS, NEG
from .base_rule_group_test_setup import BaseRuleGroupTestSetup
from ..models import HivCareAdherence
from ..classes.rule_group_utilities import *


class TestRuleGroupUtilities(BaseRuleGroupTestSetup):

    def test_art_naive_bhs(self):
        # previously on art at bhs and currently on art at ahs, no vl
        from ..classes import SubjectStatusHelper
        from ..models import SubjectVisit

        def func_previous_visit_instance(visit_instance):
            """ Returns subject_visit 1 year from the current """
            try:
                registered_subject = visit_instance.appointment.registered_subject
                previous_time_point = visit_instance.appointment.visit_definition.time_point - 1
                previous_appointment = Appointment.objects.get(registered_subject=registered_subject,
                                                               visit_definition__time_point=previous_time_point)
                return SubjectVisit.objects.get(appointment=previous_appointment)
            except Appointment.DoesNotExist:
                return None
            except SubjectVisit.DoesNotExist:
                return None
            except AttributeError:
                return None

        def func_art_naive(visit_instance):
            # This is the same method used to calculate on_naive as in the rule_groups
            """Returns True if the participant is NOT on art or cannot
            be confirmed to be on art."""
            subject_status_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=False)
            art_naive = (not subject_status_helper.on_art) and subject_status_helper.hiv_result == POS
            return art_naive

        def func_on_art(visit_instance):
            # This is the same method used to calculate on_art as in the rule_groups
            """Returns True if the participant is NOT on art or cannot
            be confirmed to be on art."""
            subject_status_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=False)
            art_naive = subject_status_helper.on_art and subject_status_helper.hiv_result == POS
            return art_naive

            self.subject_visit_male_T0 = self.baseline_subject_visit

            self._hiv_result = self.hiv_result(POS, self.subject_visit_male_T0)
            # add HivCarAdherence,
            HivCareAdherence.objects.create(
                subject_visit=self.subject_visit_male_T0,
                first_positive=None,
                medical_care='Yes',
                ever_recommended_arv='Yes',
                ever_taken_arv='Yes',
                on_arv='Yes',
                arv_evidence='Yes',  # this is the rule field
                )

            self.assertEqual(True, func_on_art(self.subject_visit_male_T0))

            self.subject_visit_male = self.annual_subject_visit

            self._hiv_result = self.hiv_result(POS, self.subject_visit_male)
            # add HivCarAdherence,
            HivCareAdherence.objects.create(
                subject_visit=self.subject_visit_male,
                first_positive=None,
                medical_care='No',
                ever_recommended_arv='No',
                ever_taken_arv='No',
                on_arv='No',
                arv_evidence='No',  # this is the rule field
                )

            self.assertEqual(True, func_on_art(func_previous_visit_instance(self.subject_visit_male)))

            self.assertEqual(True, func_art_naive(self.subject_visit_male))

    def test_art_naive_ahs(self):
        # What is the objective of this test??, it does not satisfy the test title.
        # previously on art at bhs and currently on art at ahs, no vl
        from edc.subject.appointment.models import Appointment
        from ..classes import SubjectStatusHelper
        from ..models import SubjectVisit

        def func_previous_visit_instance(visit_instance):
            """ Returns subject_visit 1 year from the current """
            try:
                registered_subject = visit_instance.appointment.registered_subject
                previous_time_point = visit_instance.appointment.visit_definition.time_point - 1
                previous_appointment = Appointment.objects.get(registered_subject=registered_subject,
                                                               visit_definition__time_point=previous_time_point)
                return SubjectVisit.objects.get(appointment=previous_appointment)
            except Appointment.DoesNotExist:
                return None
            except SubjectVisit.DoesNotExist:
                return None
            except AttributeError:
                return None

        def subject_status_helper(visit_instance, status):
            """Returns True if the participant is NOT on art or cannot
            be confirmed to be on art."""
            subject_status_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=False)
            return subject_status_helper.hiv_result == status

        self.subject_visit_male_T0 = self.baseline_subject_visit

        self._hiv_result = self.hiv_result(NEG, self.subject_visit_male_T0)

        self.assertEqual(True, subject_status_helper(self.subject_visit_male_T0, NEG))

        self.subject_visit_male = self.annual_subject_visit

        self._hiv_result = self.hiv_result(POS, self.subject_visit_male)

        self.assertEqual(True, subject_status_helper(self.subject_visit_male, POS))

        self.assertEqual(True, subject_status_helper(func_previous_visit_instance(self.subject_visit_male), NEG))
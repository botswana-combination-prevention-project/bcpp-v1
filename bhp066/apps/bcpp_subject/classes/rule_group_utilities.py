from edc.subject.appointment.models import Appointment
from edc_constants.constants import POS, NEG, IND
from edc_constants.constants import NO

from ..constants import BASELINE_CODES
from ..models import SubjectVisit, Circumcised, HicEnrollment, HivTestingHistory
from ..classes import SubjectStatusHelper


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


def func_is_baseline(visit_instance):
    if visit_instance and visit_instance.appointment.visit_definition.code in BASELINE_CODES:
        return True
    return False


def func_is_annual(visit_instance):
    if visit_instance.appointment.visit_definition.code not in BASELINE_CODES:
        return True
    return False


def func_art_naive(visit_instance):
    """Returns True if the participant is NOT on art or cannot
    be confirmed to be on art."""
    subject_status_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=False)
    art_naive = not subject_status_helper.on_art and subject_status_helper.hiv_result == POS
    return art_naive


def func_on_art(visit_instance):
    """Returns True if the participant is on art or cannot
    be confirmed to be on art."""
    subject_status_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=False)
    art_naive = subject_status_helper.on_art and subject_status_helper.hiv_result == POS
    return art_naive


def func_rbd_ahs(visit_instance):
    """Returns True if the participant is on art at ahs"""
    if not func_is_baseline(visit_instance):
        if func_hiv_negative_today(func_previous_visit_instance(visit_instance)):
            return False
        else:
            return True
    else:
        return False


def func_require_pima(visit_instance):
    """Returns True or False for doing PIMA based on hiv status and art status at each survey."""
    if func_is_baseline(visit_instance) and func_art_naive(visit_instance):
        return True
    # Hiv+ve at enrollment, art naive at enrollment
    elif art_naive_at_enrollment(visit_instance):
        return True
    # Hiv -ve at enrollment, now changed to Hiv +ve
    elif sero_converter(visit_instance) and func_art_naive(visit_instance):
        return True
    return False


def func_known_pos(visit_instance):
    """Returns True if participant is NOT a newly diagnosed POS as determined
    by the SubjectStatusHelper.new_pos method."""
    subject_status_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=False)
    known_pos = subject_status_helper.new_pos is False
    return known_pos


def func_circumcision(visit_instance):
    try:
        Circumcised.objects.get(subject_visit=func_previous_visit_instance(visit_instance))
    except Circumcised.DoesNotExist:
        return False
    return True


def func_show_hic_enrollment(visit_instance):
    """ If the participant still test HIV NEG and was not HIC enrolled then HIC should be REQUIRED. """
    past_visit = func_previous_visit_instance(visit_instance)
    if func_hiv_negative_today(visit_instance) and not func_hic_enrolled(past_visit):
        return True
    else:
        return False


def func_show_microtube(visit_instance):
    show_micro = False
    past_visit = func_previous_visit_instance(visit_instance)
    if func_hic_enrolled(past_visit) and func_hiv_positive_today(visit_instance):
        show_micro = True
    elif not func_hic_enrolled(past_visit) and func_hiv_positive_today(visit_instance):
        show_micro = False
    elif func_known_pos_in_prev_year(visit_instance):
        show_micro = False
    elif func_hiv_positive_today(visit_instance) and not past_visit:
        show_micro = False
    else:
        show_micro = True
    return show_micro


def func_todays_hiv_result_required(visit_instance):
    """Returns True if the an HIV test is required."""
    subject_status_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=False)
    if subject_status_helper.todays_hiv_result and not func_known_pos_in_prev_year(visit_instance):
        return True
    if not func_hiv_positive_today(visit_instance) and not func_known_pos_in_prev_year(visit_instance):
        return True
    return False


def func_hiv_negative_today(visit_instance):
    """Returns True if the participant tests negative today."""
    hiv_result = SubjectStatusHelper(visit_instance, use_baseline_visit=False).hiv_result
    return hiv_result == NEG


def func_hiv_indeterminate_today(visit_instance):
    """Returns True if the participant tests indeterminate today."""
    hiv_result = SubjectStatusHelper(visit_instance, use_baseline_visit=False).hiv_result
    return hiv_result == IND


def func_hiv_positive_today(visit_instance):
    """Returns True if the participant is known or newly diagnosed HIV positive."""
    hiv_result = SubjectStatusHelper(visit_instance, use_baseline_visit=False).hiv_result
    return hiv_result == POS


def func_hiv_positive_today_ahs(visit_instance):
    """Returns True if  """
    if func_is_baseline(visit_instance):
        return func_hiv_positive_today(visit_instance)
    else:
        if func_hiv_positive_today(visit_instance) and SubjectStatusHelper(visit_instance).on_art:
            return True
    return False


def func_hic_enrolled(visit_instance):
    try:
        HicEnrollment.objects.get(subject_visit=visit_instance, hic_permission='Yes')
    except HicEnrollment.DoesNotExist:
        return False
    return True


def func_hic_not_enrolled(visit_instance):
    try:
        HicEnrollment.objects.get(subject_visit=visit_instance, hic_permission='No')
    except HicEnrollment.DoesNotExist:
        return False
    return True


def func_hic(visit_instance):
    past_visit = func_previous_visit_instance(visit_instance)
    if func_hic_enrolled(past_visit) or func_hic_not_enrolled(past_visit):
        return True
    return False


def func_hiv_result_neg_baseline(visit_instance):
    """ Returns HIV negative result """
    subject_status_helper = SubjectStatusHelper(func_previous_visit_instance(visit_instance))
    return True if subject_status_helper.hiv_result == NEG else False


def func_baseline_hiv_positive_today(visit_instance):
    """Returns the baseline visit instance."""
    return SubjectStatusHelper(visit_instance, use_baseline_visit=True).hiv_result == POS


def func_baseline_hiv_positive_and_documentation_pos(visit_instance):
    """Returns the baseline visit instance."""
    subject_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=True)
    return (subject_helper.hiv_result == POS and
            subject_helper.direct_hiv_pos_documentation or
            not subject_helper.direct_hiv_pos_documentation)


def func_baseline_hiv_positive_and_not_on_art(visit_instance):
    """Returns the baseline visit instance."""
    baseline_visit_instance = func_previous_visit_instance(visit_instance)
    subject_helper = SubjectStatusHelper(baseline_visit_instance)
    return subject_helper.hiv_result == POS and not subject_helper.on_art


def func_baseline_pos_and_testreview_documentation_pos(visit_instance):
    """Returns the baseline visit instance."""
    subject_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=True)
    return subject_helper.hiv_result == POS and subject_helper.direct_hiv_pos_documentation


def func_baseline_vl_drawn(visit_instance):
    """Returns the baseline visit instance."""
    return SubjectStatusHelper(visit_instance, use_baseline_visit=True).vl_sample_drawn


def func_baseline_rbd_drawn(visit_instance):
    """Returns the baseline visit instance."""
    return SubjectStatusHelper(visit_instance, use_baseline_visit=True).rbd_sample_drawn


def func_baseline_pima_keyed(visit_instance):
    return SubjectStatusHelper(visit_instance, use_baseline_visit=True).pima_instance


def func_baseline_hiv_care_adherance_keyed(visit_instance):
    return SubjectStatusHelper(visit_instance, use_baseline_visit=True).hiv_care_adherence_instance


def func_not_required(visit_instance):
    """Returns True (always)."""
    return True


def func_known_pos_in_prev_year(visit_instance):
    past_visit = func_previous_visit_instance(visit_instance)
    pos_in_yr1 = func_hiv_positive_today(past_visit) or func_known_pos(past_visit)
    return pos_in_yr1


def func_no_verbal_hiv_result(visit_instance):
    """Returns True if verbal_hiv_positive response is not POS or NEG."""
    return SubjectStatusHelper(visit_instance).verbal_hiv_result not in ['POS', 'NEG']


def is_gender_female(visit_instance):
    """Returns True if gender from RegisteredSubject is Female."""
    return visit_instance.appointment.registered_subject.gender.lower() == 'f'


def circumsised_in_past(visit_instance):
    past_visit = func_previous_visit_instance(visit_instance)
    return Circumcised.objects.filter(subject_visit=past_visit).exists()


def func_should_not_show_circumsition(visit_instance):
    show_cicumsition = is_gender_female(visit_instance) or circumsised_in_past(visit_instance)
    return show_cicumsition


def is_gender_male(visit_instance):
    """Returns True if gender from RegisteredSubject is Male."""
    return visit_instance.appointment.registered_subject.gender.lower() == 'm'


def evaluate_ever_had_sex_for_female(visit_instance):
    """Returns True if sexual_behaviour.ever_sex is Yes and this is a female."""
    from ..models import SexualBehaviour
    sexual_behaviour = SexualBehaviour.objects.get(subject_visit=visit_instance)
    if visit_instance.appointment.registered_subject.gender.lower() == 'm':
        return False
    # if we come here then gender must be FEMALE
    elif sexual_behaviour.ever_sex.lower() == 'yes':
        return True
    return False


def first_enrolled(visit_instance):
    """ Returns true if visit_instance is the visit of first enrollment. """
    # visit_instance is the visit of first enrollment if no other visit exists prior to it.
    if func_previous_visit_instance(visit_instance):
        return False
    return True


def art_naive_at_enrollment(visit_instance):
    """ visit_instance is T3, then prev_visit1 is T2 and prev_visit2 is Baseline.
        visit_instance is T2, then prev_visit1 is T1 and prev_visit2 is None.
        visit_instance is T0, then prev_visit1 is None and prev_visit2 is None. """
    prev_visit1 = func_previous_visit_instance(visit_instance)
    prev_visit2 = func_previous_visit_instance(prev_visit1)
    if first_enrolled(prev_visit1) and func_art_naive(prev_visit1):
        return True
    elif first_enrolled(prev_visit2) and func_art_naive(prev_visit2):
        return True
    return False


def sero_converter(visit_instance):
    """ previously NEG and currently POS """
    return True if (func_hiv_negative_today(func_previous_visit_instance(visit_instance)) and
                    func_hiv_positive_today(visit_instance)) else False


def func_rbd(visit_instance):
    """Returns True or False to indicate a participant should be offered an rbd."""
    # if pos at bhs then return true
    if func_hiv_positive_today(visit_instance) and not func_baseline_rbd_drawn(visit_instance):
        return True
    return False


def func_vl(visit_instance):
    """Returns True  or False to indicate participant needs to be offered a viral load."""
    if func_is_baseline(visit_instance):
        return func_hiv_positive_today(visit_instance)
    # Hiv+ve at enrollment, art naive at enrollment
    elif art_naive_at_enrollment(visit_instance):
        return True
    # Hiv -ve at enrollment, now changed to Hiv +ve
    elif sero_converter(visit_instance):
        return True
    return False


def func_poc_vl(visit_instance):
    """Returns True or False to indicate participant needs to be offered a POC viral load."""
    if not func_art_naive(visit_instance):
        return True
    return False


def hiv_testing_history(visit_instance):
    try:
        hiv_testing = HivTestingHistory.objects.get(subject_visit=visit_instance)
    except HivTestingHistory.DoesNotExist:
        return False
    return hiv_testing.has_tested == NO


def func_hiv_untested(visit_instance):
    if func_is_baseline(visit_instance):
        return hiv_testing_history(visit_instance)
    return False

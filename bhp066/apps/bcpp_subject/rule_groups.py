from edc.constants import POS, NEG, IND

from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import (RuleGroup, site_rule_groups, ScheduledDataRule,
                                             Logic, RequisitionRule)
from edc.subject.appointment.models import Appointment

from .classes import SubjectStatusHelper

from .models import (SubjectVisit, ResourceUtilization, HivTestingHistory,
                     SexualBehaviour, HivCareAdherence, Circumcision, Circumcised,
                     HivTestReview, ReproductiveHealth, MedicalDiagnoses,
                     HivResult, HivResultDocumentation, ElisaHivResult, HicEnrollment)
from apps.bcpp_subject.constants import BASELINE_CODES


def func_baseline_visit_instance(visit_instance):
    """ Returns subject_visit for baseline """
    try:
        registered_subject = visit_instance.appointment.registered_subject
        baseline_appointment = Appointment.objects.get(
            registered_subject=registered_subject, visit_definition__time_point=0)
        return SubjectVisit.objects.get(appointment=baseline_appointment)
    except Appointment.DoesNotExist:
        return SubjectVisit.objects.none()
    except SubjectVisit.DoesNotExist:
        return SubjectVisit.objects.none()


def func_is_baseline(visit_instance):
    if visit_instance.appointment.visit_definition.code in BASELINE_CODES:
        return True
    return False


def func_is_annual(visit_instance):
    if visit_instance.appointment.visit_definition.code not in BASELINE_CODES:
        return True
    return False


def func_art_naive(visit_instance):
    """Returns True if the participant is NOT on art or cannot
    be confirmed to be on art."""
    subject_status_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=True)
    art_naive = not subject_status_helper.on_art and subject_status_helper.hiv_result == POS
    if art_naive:
        subject_status_helper = SubjectStatusHelper(visit_instance)
        art_naive = not subject_status_helper.on_art and subject_status_helper.hiv_result == POS
    return art_naive


def func_require_pima_hiv_care_ad(visit_instance):
    past_visit = func_baseline_visit_instance(visit_instance)
    return func_art_naive(visit_instance) and not func_know_pos_in_yr_1(past_visit)


def func_known_pos(visit_instance):
    """Returns True if participant is NOT a newly diagnosed POS as determined
    by the SubjectStatusHelper.new_pos method."""
    subject_status_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=True)
    known_pos = subject_status_helper.new_pos is False
    if not known_pos:
        subject_status_helper = SubjectStatusHelper(visit_instance)
        known_pos = subject_status_helper.new_pos is False
    return known_pos


def func_circumcision(visit_instance):
    try:
        Circumcised.objects.get(subject_visit=func_baseline_visit_instance(visit_instance))
    except Circumcised.DoesNotExist:
        return False
    return True


def func_show_hic_enrollment(visit_instance):
    past_visit = func_baseline_visit_instance(visit_instance)
    if func_hiv_negative_today(visit_instance) and not func_hic_keyed(past_visit):
        return True
    else:
        return False


def func_todays_hiv_result_required(visit_instance):
    """Returns True if the an HIV test is required."""
    subject_status_helper = SubjectStatusHelper(visit_instance, use_baseline_visit=True)
    if subject_status_helper.todays_hiv_result and not func_know_pos_in_yr_1(visit_instance):
        return True
    if not func_hiv_positive_today(visit_instance) and not func_know_pos_in_yr_1(visit_instance):
        return True
    return False


def func_hiv_negative_today(visit_instance):
    """Returns True if the participant tests negative today."""
    hiv_result = SubjectStatusHelper(visit_instance, use_baseline_visit=True).hiv_result
    return hiv_result == NEG


def func_hiv_indeterminate_today(visit_instance):
    """Returns True if the participant tests indeterminate today."""
    hiv_result = SubjectStatusHelper(visit_instance, use_baseline_visit=True).hiv_result
    return hiv_result == IND


def func_hiv_positive_today(visit_instance):
    """Returns True if the participant is known or newly diagnosed HIV positive."""
    hiv_result = SubjectStatusHelper(visit_instance, use_baseline_visit=True).hiv_result
    return hiv_result == POS


def func_hic_keyed(visit_instance):
    try:
        HicEnrollment.objects.get(subject_visit=visit_instance)
    except HicEnrollment.DoesNotExist:
        return False
    return True


def func_hiv_result_neg_baseline(visit_instance):
    """ Returns HIV negative result """
    subject_status_helper = SubjectStatusHelper(func_baseline_visit_instance(visit_instance))
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
    baseline_visit_instance = func_baseline_visit_instance(visit_instance)
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


def func_not_required(visit_instance):
    """Returns True (always)."""
    return True


def func_know_pos_in_yr_1(visit_instance):
    past_visit = func_baseline_visit_instance(visit_instance)
    return func_hiv_positive_today(past_visit) or func_known_pos(past_visit)


def func_no_verbal_hiv_result(visit_instance):
    """Returns True if verbal_hiv_positive response is not POS or NEG."""
    return SubjectStatusHelper(visit_instance).verbal_hiv_result not in ['POS', 'NEG']


def is_gender_female(visit_instance):
    """Returns True if gender from RegisteredSubject is Female."""
    return visit_instance.appointment.registered_subject.gender.lower() == 'f'


def circumsised_in_past(visit_instance):
    past_visit = func_baseline_visit_instance(visit_instance)
    return Circumcised.objects.filter(subject_visit=past_visit).exists()


def func_should_not_show_circumsition(visit_instance):
    return is_gender_female(visit_instance) or circumsised_in_past(visit_instance)


def is_gender_male(visit_instance):
    """Returns True if gender from RegisteredSubject is Male."""
    return visit_instance.appointment.registered_subject.gender.lower() == 'm'


def evaluate_ever_had_sex_for_female(visit_instance):
    """Returns True if sexual_behaviour.ever_sex is Yes and this is a female."""
    sexual_behaviour = SexualBehaviour.objects.get(subject_visit=visit_instance)
    if visit_instance.appointment.registered_subject.gender.lower() == 'm':
        return False
    # if we come here then gender must be FEMALE
    elif sexual_behaviour.ever_sex.lower() == 'yes':
        return True
    return False


class RegisteredSubjectRuleGroup(RuleGroup):

    gender_circumsion = ScheduledDataRule(
        logic=Logic(
            predicate=func_should_not_show_circumsition,
            consequence='not_required',
            alternative='new'),
        target_model=['circumcision', 'circumcised', 'uncircumcised'])

    gender_menopause = ScheduledDataRule(
        logic=Logic(
            predicate=is_gender_male,
            consequence='not_required',
            alternative='new'),
        target_model=['reproductivehealth', 'pregnancy', 'nonpregnancy'])

    known_pos_in_y1 = ScheduledDataRule(
        logic=Logic(
            predicate=func_know_pos_in_yr_1,
            consequence='not_required',
            alternative='new'),
        target_model=['hivtestreview', 'hivtested', 'hivtestinghistory', 'hivresultdocumentation', 'hivresult', 'pima'])

    require_microtube = RequisitionRule(
        logic=Logic(
            predicate=func_know_pos_in_yr_1,
            consequence='not_required',
            alternative='new'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Microtube'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = None
        source_model = RegisteredSubject

site_rule_groups.register(RegisteredSubjectRuleGroup)


class ResourceUtilizationRuleGroup(RuleGroup):

    out_patient = ScheduledDataRule(
        logic=Logic(
            predicate=(('out_patient', 'equals', 'no'), ('out_patient', 'equals', 'Refuse', 'or')),
            consequence='not_required',
            alternative='new'),
        target_model=['outpatientcare'])

    hospitalized = ScheduledDataRule(
        logic=Logic(
            predicate=('hospitalized', 'equals', 0),
            consequence='not_required',
            alternative='new'),
        target_model=['hospitaladmission'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = ResourceUtilization

site_rule_groups.register(ResourceUtilizationRuleGroup)


class HivTestingHistoryRuleGroup(RuleGroup):

    pima_for_art_naive = ScheduledDataRule(
        logic=Logic(
            predicate=func_art_naive,
            consequence='new',
            alternative='not_required'),
        target_model=['pima'])

    has_record = ScheduledDataRule(
        logic=Logic(
            predicate=('has_record', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivtestreview'])

    has_tested = ScheduledDataRule(
        logic=Logic(
            predicate=('has_tested', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivtested'])

    hiv_untested = ScheduledDataRule(
        logic=Logic(
            predicate=('has_tested', 'equals', 'No'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivuntested'],
        runif=func_is_baseline)

    other_record = ScheduledDataRule(
        logic=Logic(
            predicate=('other_record', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivresultdocumentation'])

    require_todays_hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='new',
            alternative='not_required'),
        target_model=['hivresult'],
        runif=func_is_baseline)

    verbal_hiv_result_hiv_care_baseline = ScheduledDataRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'equals', 'POS'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivcareadherence'],
        runif=func_is_baseline)

    verbal_hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=func_known_pos,
            consequence='new',
            alternative='not_required'),
        target_model=['hivmedicalcare', 'positiveparticipant'])

    verbal_response = ScheduledDataRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'equals', 'NEG'),
            consequence='new',
            alternative='not_required'),
        target_model=['stigma', 'stigmaopinion'])

    verbal_result_response = ScheduledDataRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'equals', 'NEG'),
            consequence='not_required',
            alternative='new'),
        target_model=['positiveparticipant', 'hivmedicalcare'])

    other_response = ScheduledDataRule(
        logic=Logic(
            predicate=func_no_verbal_hiv_result,
            consequence='not_required',
            alternative='none'),
        target_model=['hivcareadherence', 'hivmedicalcare', 'positiveparticipant', 'stigma', 'stigmaopinion'])

    def method_result(self):
        return True

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivTestingHistory
site_rule_groups.register(HivTestingHistoryRuleGroup)


class ReviewPositiveRuleGroup(RuleGroup):
    pima_for_art_naive = ScheduledDataRule(
        logic=Logic(
            predicate=func_art_naive,
            consequence='new',
            alternative='not_required'),
        target_model=['pima'])

    recorded_hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='not_required',
            alternative='new'),
        target_model=['hivcareadherence', 'hivmedicalcare', 'positiveparticipant'])

    recorded_hivresult = ScheduledDataRule(
        logic=Logic(
            predicate=('recorded_hiv_result', 'equals', 'NEG'),
            consequence='new',
            alternative='not_required'),
        target_model=['stigma', 'stigmaopinion'])

    require_todays_hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='new',
            alternative='not_required'),
        target_model=['hivresult'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivTestReview
site_rule_groups.register(ReviewPositiveRuleGroup)


class HivCareAdherenceRuleGroup(RuleGroup):

    medical_care = ScheduledDataRule(
        logic=Logic(
            predicate=('medical_care', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivmedicalcare'])

    pima_for_art_naive = ScheduledDataRule(
        logic=Logic(
            predicate=func_require_pima_hiv_care_ad,
            consequence='new',
            alternative='not_required'),
        target_model=['pima'])

    require_todays_hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='new',
            alternative='not_required'),
        target_model=['hivresult'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivCareAdherence
site_rule_groups.register(HivCareAdherenceRuleGroup)


# class AnnualHivCareAdherenceRuleGroup(RuleGroup):
# 
#     require_hiv_medical_care_hiv_health_care_costs = ScheduledDataRule(
#         logic=Logic(
#             predicate=func_baseline_hiv_positive_and_not_on_art,
#             consequence='new',
#             alternative='not_required'),
#         target_model=['hivmedicalcare', 'hivhealthcarecosts'],
#         runif=func_is_annual)
# 
#     class Meta:
#         app_label = 'bcpp_subject'
#         source_fk = (SubjectVisit, 'subject_visit')
#         source_model = HivCareAdherence
# site_rule_groups.register(AnnualHivCareAdherenceRuleGroup)


class SexualBehaviourRuleGroup(RuleGroup):

    partners = ScheduledDataRule(
        logic=Logic(
            predicate=('last_year_partners', 'gte', 1),
            consequence='new',
            alternative='not_required'),
        target_model=['monthsrecentpartner', 'monthssecondpartner', 'monthsthirdpartner'])

    last_year_partners = ScheduledDataRule(
        logic=Logic(
            predicate=('last_year_partners', 'gte', 2),
            consequence='new',
            alternative='not_required'),
        target_model=['monthssecondpartner'])

    more_partners = ScheduledDataRule(
        logic=Logic(
            predicate=('last_year_partners', 'gte', 3),
            consequence='new',
            alternative='not_required'),
        target_model=['monthsthirdpartner'])

    ever_sex = ScheduledDataRule(
        logic=Logic(
            predicate=evaluate_ever_had_sex_for_female,
            consequence='new',
            alternative='not_required'),
        target_model=['reproductivehealth', 'pregnancy', 'nonpregnancy'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = SexualBehaviour
site_rule_groups.register(SexualBehaviourRuleGroup)


class CircumcisionRuleGroup(RuleGroup):

    circumcised = ScheduledDataRule(
        logic=Logic(
            predicate=('circumcised', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['circumcised'])

    uncircumcised = ScheduledDataRule(
        logic=Logic(
            predicate=('circumcised', 'equals', 'No'),
            consequence='new',
            alternative='not_required'),
        target_model=['uncircumcised'])

    # if circumcised do not require circumcision forms again
    circumcised_annual = ScheduledDataRule(
        logic=Logic(
            predicate=func_circumcision,
            consequence='not_required',
            alternative='new'),
        target_model=['circumcised', 'uncircumcised'],
        runif=func_is_annual)

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = Circumcision
site_rule_groups.register(CircumcisionRuleGroup)


class ReproductiveRuleGroup(RuleGroup):

    currently_pregnant = ScheduledDataRule(
        logic=Logic(
            predicate=(('currently_pregnant', 'equals', 'Yes'), ('menopause', 'equals', 'No', 'and')),
            consequence='new',
            alternative='not_required'),
        target_model=['pregnancy'])

    non_pregnant = ScheduledDataRule(
        logic=Logic(
            predicate=(('currently_pregnant', 'equals', 'No'), ('menopause', 'equals', 'No', 'and')),
            consequence='new',
            alternative='not_required'),
        target_model=['nonpregnancy'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = ReproductiveHealth
site_rule_groups.register(ReproductiveRuleGroup)


class MedicalDiagnosesRuleGroup(RuleGroup):
    """"Allows the heartattack, cancer, tb forms to be made available whether or not the participant
    has a record. see redmine 314."""
    heart_attack_record = ScheduledDataRule(
        logic=Logic(
            predicate=('heart_attack_record', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['heartattack'])

    cancer_record = ScheduledDataRule(
        logic=Logic(
            predicate=('cancer_record', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['cancer'])

    tb_record_tubercolosis = ScheduledDataRule(
        logic=Logic(
            predicate=('tb_record', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['tubercolosis'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = MedicalDiagnoses
site_rule_groups.register(MedicalDiagnosesRuleGroup)


class BaseRequisitionRuleGroup(RuleGroup):
    """Ensures an RBD requisition if HIV result is POS."""
    rbd_vl_for_pos = RequisitionRule(
        logic=Logic(
            predicate=func_hiv_positive_today,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Research Blood Draw', 'Viral Load'], )

    """Ensures a Microtube is not required for POS."""
    microtube_for_neg = RequisitionRule(
        logic=Logic(
            predicate=func_hiv_positive_today,
            consequence='not_required',
            alternative='new'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Microtube'], )

    pima_for_art_naive = ScheduledDataRule(
        logic=Logic(
            predicate=func_art_naive,
            consequence='new',
            alternative='not_required'),
        target_model=['pima'])

    hic = ScheduledDataRule(
        logic=Logic(
            predicate=func_show_hic_enrollment,
            consequence='new',
            alternative='not_required'),
        target_model=['hicenrollment'],
        runif=func_is_baseline)

    class Meta:
        abstract = True


class RequisitionRuleGroup1(BaseRequisitionRuleGroup):

    """Ensures an ELISA blood draw requisition if HIV result is IND."""
    elisa_for_ind = RequisitionRule(
        logic=Logic(
            predicate=func_hiv_indeterminate_today,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['ELISA', ], )

    """Ensures a venous blood draw requisition is required if insufficient
    volume in the capillary (microtube)."""
    venous_for_vol = RequisitionRule(
        logic=Logic(
            predicate=(('insufficient_vol', 'equals', 'Yes'), ('blood_draw_type', 'equals', 'venous', 'or'),),
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Venous (HIV)'], )

    serve_sti_form = ScheduledDataRule(
        logic=Logic(
            predicate=func_hiv_positive_today,
            consequence='new',
            alternative='not_required'),
        target_model=['sti'])

    elisa_result = ScheduledDataRule(
        logic=Logic(
            predicate=func_hiv_indeterminate_today,
            consequence='new',
            alternative='not_required'),
        target_model=['elisahivresult'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivResult
site_rule_groups.register(RequisitionRuleGroup1)


class RequisitionRuleGroup2(BaseRequisitionRuleGroup):

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivTestingHistory
site_rule_groups.register(RequisitionRuleGroup2)


class RequisitionRuleGroup3(BaseRequisitionRuleGroup):

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivTestReview
site_rule_groups.register(RequisitionRuleGroup3)


class RequisitionRuleGroup4(BaseRequisitionRuleGroup):

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivResultDocumentation
site_rule_groups.register(RequisitionRuleGroup4)


class RequisitionRuleGroup5(BaseRequisitionRuleGroup):

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = ElisaHivResult
site_rule_groups.register(RequisitionRuleGroup5)

from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import (RuleGroup, site_rule_groups, ScheduledDataRule,
                                             Logic, RequisitionRule)

from .classes import SubjectStatusHelper

from .models import (SubjectVisit, ResourceUtilization, HivTestingHistory,
                     SexualBehaviour, HivCareAdherence, Circumcision,
                     HivTestReview, ReproductiveHealth, MedicalDiagnoses,
                     HivResult, HivResultDocumentation, ElisaHivResult)


def func_art_naive(visit_instance):
    """Returns True if the participant is NOT on art or cannot
    be confirmed to be on art."""
    subject_status_helper = SubjectStatusHelper(visit_instance)
    return not subject_status_helper.on_art and subject_status_helper.hiv_result == 'POS'


def func_known_pos(visit_instance):
    """Returns True if participant is NOT a newly diagnosed POS as determined
    by the SubjectStatusHelper.new_pos method."""
    return SubjectStatusHelper(visit_instance).new_pos is False


def func_todays_hiv_result_required(visit_instance):
    """Returns True if the an HIV test is required."""
    subject_status_helper = SubjectStatusHelper(visit_instance)
    if subject_status_helper.todays_hiv_result:
        return True
    return False if (subject_status_helper.new_pos is False) else True


def func_hiv_negative_today(visit_instance):
    """Returns True if the participant tests negative today."""
    return SubjectStatusHelper(visit_instance).hiv_result == 'NEG'


def func_hiv_indeterminate_today(visit_instance):
    """Returns True if the participant tests indeterminate today."""
    return SubjectStatusHelper(visit_instance).hiv_result == 'IND'


def func_hiv_positive_today(visit_instance):
    """Returns True if the participant is known or newly diagnosed HIV positive."""
    return SubjectStatusHelper(visit_instance).hiv_result == 'POS'


def func_not_required(visit_instance):
    """Returns True (always)."""
    return True


def func_no_verbal_hiv_result(visit_instance):
    """Returns True if verbal_hiv_positive response is not POS or NEG."""
    return SubjectStatusHelper(visit_instance).verbal_hiv_result not in ['POS', 'NEG']


def is_gender_female(visit_instance):
    """Returns True if gender from RegisteredSubject is Female."""
    return visit_instance.appointment.registered_subject.gender.lower() == 'f'


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
            predicate=is_gender_female,
            consequence='not_required',
            alternative='new'),
        target_model=['circumcision', 'circumcised', 'uncircumcised'])

    gender_menopause = ScheduledDataRule(
        logic=Logic(
            predicate=is_gender_male,
            consequence='not_required',
            alternative='new'),
        target_model=['reproductivehealth', 'pregnancy', 'nonpregnancy'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = None
        source_model = RegisteredSubject

site_rule_groups.register(RegisteredSubjectRuleGroup)


class ResourceUtilizationRuleGroup(RuleGroup):

    out_patient = ScheduledDataRule(
        logic=Logic(
            predicate=(('out_patient', 'equals', 'no'), ('out_patient', 'equals', 'REF', 'or')),
            consequence='not_required',
            alternative='new'),
        target_model=['outpatientcare'])

    hospitalized = ScheduledDataRule(
        logic=Logic(
            predicate=(('hospitalized', 'equals', ''), ('hospitalized', 'equals', 0, 'or')),
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
        target_model=['hivuntested'])

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
        target_model=['hivresult'])

    verbal_hiv_result_hiv_care = ScheduledDataRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'equals', 'POS'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivcareadherence'])

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
            predicate=func_art_naive,
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
            predicate=func_hiv_negative_today,
            consequence='new',
            alternative='not_required'),
        target_model=['hicenrollment'])

    class Meta:
        abstract = True


class RequisitionRuleGroup1(BaseRequisitionRuleGroup):

    """Ensures an ELISA blood draw requisition if HIV result is IND."""
    elisa_for_ind = RequisitionRule(
        logic=Logic(
            predicate=func_hiv_indeterminate_today,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition'), 'elisahivresult'],
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

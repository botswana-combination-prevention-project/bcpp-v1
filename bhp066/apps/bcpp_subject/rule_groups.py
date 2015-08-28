from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import (RuleGroup, site_rule_groups, ScheduledDataRule,
                                             Logic, RequisitionRule)
from .constants import PIMA_VL_TYPE, CENTRAL_SERVER

from .models import (ResourceUtilization, HivTestingHistory,
                     SexualBehaviour, HivCareAdherence, Circumcision,
                     HivTestReview, ReproductiveHealth, MedicalDiagnoses,
                     HivResult, HivResultDocumentation, ElisaHivResult)
from .classes.rule_group_utilities import *


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
            predicate=func_known_pos_in_prev_year,
            consequence='not_required',
            alternative='new'),
        target_model=['hivtestreview', 'hivtested', 'hivtestinghistory', 'hivresultdocumentation', 'hivresult'])

#     pima_naive_bhs_req_ahs = ScheduledDataRule(
#         logic=Logic(
#             predicate=func_require_pima_hiv_care_ad,
#             consequence='new',
#             alternative='not_required'),
#         target_model=['pima'])

    require_microtube = RequisitionRule(
        logic=Logic(
            predicate=func_show_microtube,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Microtube'])

    vl_for_pos = RequisitionRule(
        logic=Logic(
            predicate=func_vl,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Viral Load'], )

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
            predicate=func_require_pima_hiv_care_ad,
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
            predicate=func_show_microtube,
            consequence='new',
            alternative='not_required'),
        target_model=['hivresult'])

    verbal_hiv_result_hiv_care_baseline = ScheduledDataRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'equals', 'POS'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivcareadherence', 'positiveparticipant', 'hivmedicalcare', 'hivhealthcarecosts'])

    verbal_response = ScheduledDataRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'equals', 'NEG'),
            consequence='new',
            alternative='not_required'),
        target_model=['stigma', 'stigmaopinion'])

#     verbal_result_response = ScheduledDataRule(
#         logic=Logic(
#             predicate=('verbal_hiv_result', 'equals', 'POS'),
#             consequence='new',
#             alternative='not_required'),
#         target_model=['positiveparticipant', 'hivmedicalcare', 'hivhealthcarecosts'])

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
            predicate=func_require_pima_hiv_care_ad,
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
            predicate=func_show_microtube,
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

    pimavl_for_art_naive = ScheduledDataRule(
        logic=Logic(
            predicate=func_poc_vl,
            consequence='new',
            alternative='not_required'),
        target_model=['pimavl'])

#     vl_for_known_pos = RequisitionRule(
#         logic=Logic(
#             predicate=func_art_naive,
#             consequence='new',
#             alternative='not_required'),
#         target_model=[('bcpp_lab', 'subjectrequisition')],
#         target_requisition_panels=['Viral Load'],)

    require_todays_hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=func_show_microtube,
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

#     not_sure_circumcised = ScheduledDataRule(
#         logic=Logic(
#             predicate=('circumcised', 'equals', 'Not Sure'),
#             consequence='not_required',
#             alternative='none'),
#         target_model=['uncircumcised', 'circumcised'])

    # if circumcised do not require circumcision forms again
#     circumcised_annual = ScheduledDataRule(
#         logic=Logic(
#             predicate=func_circumcision,
#             consequence='not_required',
#             alternative='new'),
#         target_model=['circumcised', 'uncircumcised'])

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
    rbd_for_pos = RequisitionRule(
        logic=Logic(
            predicate=func_rbd,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Research Blood Draw'], )

    vl_for_pos = RequisitionRule(
        logic=Logic(
            predicate=func_vl,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Viral Load'], )

#     vl_for_known_pos = RequisitionRule(
#         logic=Logic(
#             predicate=func_rbd_ahs,
#             consequence='not_required',
#             alternative='new'),
#         target_model=[('bcpp_lab', 'subjectrequisition')],
#         target_requisition_panels=['Research Blood Draw'],)

    """Ensures a Microtube is not required for POS."""
    microtube_for_neg = RequisitionRule(
        logic=Logic(
            predicate=func_show_microtube,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Microtube'], )

    pima_for_art_naive = ScheduledDataRule(
        logic=Logic(
            predicate=func_require_pima_hiv_care_ad,
            consequence='new',
            alternative='not_required'),
        target_model=['pima'])

    pimavl_for_art_naive = ScheduledDataRule(
        logic=Logic(
            predicate=func_poc_vl,
            consequence='new',
            alternative='not_required'),
        target_model=['pimavl'])

    hic = ScheduledDataRule(
        logic=Logic(
            predicate=func_show_hic_enrollment,
            consequence='new',
            alternative='not_required'),
        target_model=['hicenrollment'])

#     known_pos_circumcised = ScheduledDataRule(
#         logic=Logic(
#             predicate=func_should_not_show_circumsition,
#             consequence='not_required',
#             alternative='new'),
#         target_model=['circumcised', 'uncircumcised', 'circumcision'])

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

    known_pos_circumcised_2 = ScheduledDataRule(
    logic=Logic(
        predicate=func_should_not_show_circumsition,
        consequence='not_required',
        alternative='new'),
    target_model=['circumcised', 'uncircumcised', 'circumcision'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivTestReview
site_rule_groups.register(RequisitionRuleGroup3)


class RequisitionRuleGroup4(BaseRequisitionRuleGroup):

    known_pos_circumcised_3 = ScheduledDataRule(
    logic=Logic(
        predicate=func_should_not_show_circumsition,
        consequence='not_required',
        alternative='new'),
    target_model=['circumcised', 'uncircumcised', 'circumcision'])

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

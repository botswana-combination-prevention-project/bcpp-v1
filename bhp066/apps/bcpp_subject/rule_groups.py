from edc.subject.rule_groups.classes import RuleGroup, site_rule_groups, ScheduledDataRule, Logic, RequisitionRule
from edc.subject.registration.models import RegisteredSubject

from .models import (SubjectVisit, ResourceUtilization, HivTestingHistory,
                    SexualBehaviour, HivCareAdherence, Circumcision,
                    HivTestReview, ReproductiveHealth, MedicalDiagnoses,
                    HivResult, HivResultDocumentation, Pima)


class RegisteredSubjectRuleGroup(RuleGroup):

    gender_circumsion = ScheduledDataRule(
        logic=Logic(
            predicate=('gender', 'equals', 'f'),
            consequence='not_required',
            alternative='new'),
        target_model=['circumcision', 'circumcised', 'uncircumcised'])

    gender_menopause = ScheduledDataRule(
        logic=Logic(
            predicate=('gender', 'equals', 'm'),
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


# Would probably be useful for T12 survey
# class SubjectDeathRuleGroup(RuleGroup):
#
#     death = AdditionalDataRule(
#         logic=Logic(
#             predicate=('reason', 'equals', 'death'),
#             consequence='required',
#             alternative='not_required'),
#         target_model=['subjectoffstudy', 'subjectdeath'])
#
#     class Meta:
#         app_label = 'bcpp_subject'
#         source_model = SubjectVisit
#         source_fk = (RegisteredSubject, 'registered_subject')
# site_rule_groups.register(SubjectDeathRuleGroup)


class HivTestingHistoryRuleGroup(RuleGroup):

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

#     verbal_hiv_result_and_documentation = ScheduledDataRule(
#         logic=Logic(
#             predicate=(('verbal_hiv_result', 'equals', 'POS'), ('has_record', 'equals', 'Yes', 'and')),
#             consequence='new',
#             alternative='not_required'),
#         target_model=['hivcareadherence'])

    verbal_hiv_result_for_hic = ScheduledDataRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'ne', 'POS'),
            consequence='new',
            alternative='not_required'),
        target_model=['hicenrollment', 'hivresult'])

    verbal_hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'equals', 'POS'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivcareadherence', 'hivmedicalcare', 'positiveparticipant'])

    verbal_response = ScheduledDataRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'equals', 'NEG'),
            consequence='new',
            alternative='not_required'),
        target_model=['stigma', 'stigmaopinion'])

    #TODO: including this other_response leads to results from rules from above being reset, prety much its wrong.
    #but we still need a way to handle 'IND', 'UNK',
    other_response = ScheduledDataRule(
        logic=Logic(
            predicate=(('verbal_hiv_result', 'equals', 'IND'), ('verbal_hiv_result', 'equals', 'UNK', 'or'), ('verbal_hiv_result', 'equals', 'not_answering', 'or')),
            consequence='not_required',
            alternative='new'),
        target_model=['hivcareadherence', 'hivmedicalcare', 'positiveparticipant', 'stigma', 'stigmaopinion'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivTestingHistory
site_rule_groups.register(HivTestingHistoryRuleGroup)


class HivTestReviewRuleGroup(RuleGroup):

    recorded_hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=('recorded_hiv_result', 'equals', 'POS'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivcareadherence', 'positiveparticipant', ])

    recorded_hivresult = ScheduledDataRule(
        logic=Logic(
            predicate=('recorded_hiv_result', 'equals', 'NEG'),
            consequence='new',
            alternative='not_required'),
        target_model=['stigma', 'stigmaopinion'])

    
#     other_responses = ScheduledDataRule(
#         logic=Logic(
#             predicate=(('recorded_hiv_result', 'ne', 'POS'), ('recorded_hiv_result', 'ne', 'NEG', 'and')),
#             consequence='not_required',
#             alternative='new'),
#         target_model=['hivcareadherence', 'hivmedicalcare', 'positiveparticipant', 'stigma', 'stigmaopinion'])

    # This is to make the hivresult form TODAYS HIV RESULT only available if the HIV result from the hivtestreview is POS
#     if_recorded_result_not_positive = ScheduledDataRule(
#         logic=Logic(
#             predicate=('recorded_hiv_result', 'ne', 'POS'),
#             consequence='new',
#             alternative='not_required'),
#         target_model=['hivresult',])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivTestReview
site_rule_groups.register(HivTestReviewRuleGroup)


class ReviewNotPositiveRuleGroup(RuleGroup):
    # This is to make the hivresult form TODAYS HIV RESULT only available if the HIV result from the hivtestreview is POS
    if_recorded_result_not_positive = ScheduledDataRule(
        logic=Logic(
            predicate=('recorded_hiv_result', 'ne', 'POS'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivresult', 'hicenrollment'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivTestReview
site_rule_groups.register(ReviewNotPositiveRuleGroup)


class HivDocumentationGroup(RuleGroup):
#    requires Todays HIV results form when the other HIV result documentation form  recorded result is POS
    result_recorded = ScheduledDataRule(
        logic=Logic(
            predicate=('result_recorded', 'ne', 'POS'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivresult', 'hicenrollment'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivResultDocumentation
site_rule_groups.register(HivDocumentationGroup)


class HivCareAdherenceRuleGroup(RuleGroup):

    medical_care = ScheduledDataRule(
        logic=Logic(
            predicate=('medical_care', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivmedicalcare'])
    #What if they are HIV + but not on ARV, then PIMA is not required???,seems odd.
    on_arv = ScheduledDataRule(
        logic=Logic(
            predicate=('on_arv', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['pima'])
    
#     arv_evidence = ScheduledDataRule(
#         logic=Logic(
#             predicate=('arv_evidence', 'equals', 'Yes'),
#             consequence='new',
#             alternative='not_required'),
#         target_model=['pima'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivCareAdherence
site_rule_groups.register(HivCareAdherenceRuleGroup)


class TodaysHivRuleGroup(RuleGroup):
#   confirms pima required only when HIV result from today is positive
    hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=('hiv_result', 'equals', 'POS'),
            consequence='new',
            alternative='not_required'),
        target_model=['pima'])

    hic_enrollement = ScheduledDataRule(
        logic=Logic(
            predicate=(('hiv_result', 'equals', 'POS'), ('hiv_result', 'equals', 'Declined', 'or'), ('hiv_result', 'equals', 'Not performed', 'or')),
            consequence='not_required',
            alternative='new'),
        target_model=['hicenrollment'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivResult
site_rule_groups.register(TodaysHivRuleGroup)


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


class MenopauseRuleGroup(RuleGroup):

    menopause = ScheduledDataRule(
        logic=Logic(
            predicate=('menopause', 'equals', 'Yes'),
            consequence='not_required',
            alternative='new'),
        target_model=['pregnancy', 'nonpregnancy'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = ReproductiveHealth
site_rule_groups.register(MenopauseRuleGroup)


class ReproductiveRuleGroup(RuleGroup):

    currently_pregnant = ScheduledDataRule(
        logic=Logic(
            predicate=('currently_pregnant', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['pregnancy'])

    pregnant = ScheduledDataRule(
        logic=Logic(
            predicate=('currently_pregnant', 'equals', 'No'),
            consequence='new',
            alternative='not_required'),
        target_model=['nonpregnancy'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = ReproductiveHealth
site_rule_groups.register(ReproductiveRuleGroup)


class MedicalDiagnosesRuleGroup(RuleGroup):

    heart_attack_record = ScheduledDataRule(
        logic=Logic(
            predicate=(('heart_attack_record', 'equals', 'Yes'), ('heart_attack_record', 'equals', 'No', 'or')),
            consequence='new',
            alternative='not_required'),
        target_model=['heartattack'])

    cancer_record = ScheduledDataRule(
        logic=Logic(
            predicate=(('cancer_record', 'equals', 'Yes'), ('cancer_record', 'equals', 'Yes', 'or')),
            consequence='new',
            alternative='not_required'),
        target_model=['cancer'])

    tb_record = ScheduledDataRule(
        logic=Logic(
            predicate=(('tb_record', 'equals', 'Yes'), ('tb_record', 'equals', 'No', 'or')),
            consequence='new',
            alternative='not_required'),
        target_model=['tubercolosis'])

#     sti_record = ScheduledDataRule(
#         logic=Logic(
#             predicate=('sti_record', 'equals', 'Yes'),
#             consequence='new',
#             alternative='not_required'),
#         target_model=['sti'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = MedicalDiagnoses
site_rule_groups.register(MedicalDiagnosesRuleGroup)


class RequisitionRuleGroup(RuleGroup):

#     """Ensures no requisitions if HIV result is not POS or IND."""
#     hiv_result3 = RequisitionRule(
#         logic=Logic(
#             predicate=(('hiv_result', 'equals', 'POS'), ('hiv_result', 'equals', 'IND', 'or')),
#             consequence='new',
#             alternative='not_required'),
#         target_model=[('bcpp_lab', 'subjectrequisition')],
#         target_requisition_panels=['Research Blood Draw', 'Viral Load', 'Microtube', 'Venous (HIV)', 'ELISA'], )

    """Ensures an RBD, VL and Microtube blood draw requisition if HIV result is POS."""
    hiv_result1 = RequisitionRule(
        logic=Logic(
            predicate=(('hiv_result', 'equals', 'POS'), ('hiv_result', 'equals', 'IND', 'or')),
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Research Blood Draw', 'Viral Load', 'Microtube'], )

    """Ensures an ELISA blood draw requisition if HIV result is IND."""
    hiv_result2 = RequisitionRule(
        logic=Logic(
            predicate=(('hiv_result', 'equals', 'IND'), ),
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['ELISA'], )

    """Ensures a venous blood draw requisition is required if insufficient volume in the capillary (microtube)."""
    hiv_result3 = RequisitionRule(
        logic=Logic(
            predicate=(('insufficient_vol', 'equals', 'Yes'), ('blood_draw_type', 'equals', 'venous', 'or'),),
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Venous (HIV)'], )

#     hiv_result4 = RequisitionRule(
#         logic=Logic(
#             predicate=(('blood_draw_type', 'equals', 'venous')),
#             consequence='new',
#             alternative='none'),
#         target_model=[('bcpp_lab', 'subjectrequisition')],
#         target_requisition_panels=['Venous (HIV)'], )
#     """Ensures a venous blood draw requisition is required if insufficient volume in the capillary (microtube)."""
#     hiv_result1 = RequisitionRule(
#         logic=Logic(
#             predicate=(('insufficient_vol', 'equals', 'Yes'), ('blood_draw_type', 'equals', 'venous', 'or')),
#             consequence='new',
#             alternative='not_required'),
#         target_model=[('bcpp_lab', 'subjectrequisition')],
#         target_requisition_panels=['Venous (HIV)'], )

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivResult
site_rule_groups.register(RequisitionRuleGroup)

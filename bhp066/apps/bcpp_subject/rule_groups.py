from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import RuleGroup, site_rule_groups, ScheduledDataRule, Logic, RequisitionRule

from .classes import SubjectStatusRuleHelper

from .models import (SubjectVisit, ResourceUtilization, HivTestingHistory,
                    SexualBehaviour, HivCareAdherence, Circumcision,
                    HivTestReview, ReproductiveHealth, MedicalDiagnoses,
                    HivResult, HivResultDocumentation)


def func_pima_required(visit_instance):
    """Returns True if the pima is required"""
    return SubjectStatusRuleHelper(visit_instance).pima_required


def func_todays_hiv_result_required(visit_instance):
    """Returns True if the an HIV test is required"""
    return SubjectStatusRuleHelper(visit_instance).hiv_result_required


def func_not_hiv_positive_today(visit_instance):
    """Returns True if the participant, so far, has not been determined to be positive."""
    return SubjectStatusRuleHelper(visit_instance).hiv_result != 'POS'


def func_hiv_indeterminate_today(visit_instance):
    """Returns True if the participant tests indeterminate today."""
    return SubjectStatusRuleHelper(visit_instance).hiv_result == 'IND'


def func_hiv_positive_today(visit_instance):
    """Returns True if the participant has been determinied to be either known or newly diagnosed HIV positive."""
    return SubjectStatusRuleHelper(visit_instance).hiv_result == 'POS'


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


class HivTestingHistoryRuleGroup(RuleGroup):

    pima_required = ScheduledDataRule(
        logic=Logic(
            predicate=func_pima_required,
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

    #Verbal hiv posetive with documentation, then Microtube is not reuired.
    microtube_known_pos = RequisitionRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Microtube'],)

    #Venus is not reuired untill Microtube does not have enoguh volume. That happens in HivResultReultGroup
    #Next two rules make sure its always NOT_REQUIRED when this form is being fileed.
    venus_on_required1 = RequisitionRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'equals', 'POS'),
            consequence='not_required',
            alternative='none'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Venous (HIV)'],)

    venus_on_required2 = RequisitionRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'ne', 'POS'),
            consequence='not_required',
            alternative='none'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Venous (HIV)'],)

    #ELISA is not reuired untill Microtube result is IND. That happens in HivResultReultGroup
    #Next two rules make sure its always NOT_REQUIRED when this form is being fileed.
    elisa_on_required1 = RequisitionRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'equals', 'IND'),
            consequence='not_required',
            alternative='none'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['ELISA'],)

    elisa_on_required2 = RequisitionRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'ne', 'IND'),
            consequence='not_required',
            alternative='none'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['ELISA'],)

    #Verbal posetive, then RBD and VL are required.
    rbd_vl_known_pos = RequisitionRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='not_required',
            alternative='new'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Research Blood Draw', 'Viral Load'])

    require_todays_hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='new',
            alternative='not_required'),
        target_model=['hivresult'])

    hic = ScheduledDataRule(
        logic=Logic(
            predicate=func_not_hiv_positive_today,
            consequence='new',
            alternative='not_required'),
        target_model=['hicenrollment'])

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

    other_response = ScheduledDataRule(
        logic=Logic(
            predicate=(('verbal_hiv_result', 'equals', 'IND'), ('verbal_hiv_result', 'equals', 'UNK', 'or'), ('verbal_hiv_result', 'equals', 'not_answering', 'or')),
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
    pima_required = ScheduledDataRule(
        logic=Logic(
            predicate=func_pima_required,
            consequence='new',
            alternative='not_required'),
        target_model=['pima'])

    recorded_hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='not_required',
            alternative='new'),
        target_model=['hivcareadherence', 'hivmedicalcare', 'positiveparticipant', ])

    recorded_hivresult = ScheduledDataRule(
        logic=Logic(
            predicate=('recorded_hiv_result', 'equals', 'NEG'),
            consequence='new',
            alternative='not_required'),
        target_model=['stigma', 'stigmaopinion'])

    other_responses = ScheduledDataRule(
        logic=Logic(
            predicate=(('recorded_hiv_result', 'equals', 'IND'), ('recorded_hiv_result', 'equals', 'UNK', 'or')),
            consequence='not_required',
            alternative='none'),
        target_model=['hivcareadherence', 'hivmedicalcare', 'positiveparticipant'])
    # This is to make the hivresult form TODAYS HIV RESULT only available if the HIV result from the hivtestreview is POS
    require_todays_hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='new',
            alternative='not_required'),
        target_model=['hivresult'])

    hic = ScheduledDataRule(
        logic=Logic(
            predicate=func_not_hiv_positive_today,
            consequence='new',
            alternative='not_required'),
        target_model=['hicenrollment'])

    microtube_known_pos = RequisitionRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Microtube'],)

    #Venus is not reuired untill Microtube does not have enoguh volume. That happens in HivResultReultGroup
    #Next two rules make sure its always NOT_REQUIRED when this form is being fileed.
    venus_on_required1 = RequisitionRule(
        logic=Logic(
            predicate=('recorded_hiv_result', 'equals', 'POS'),
            consequence='not_required',
            alternative='none'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Venous (HIV)'],)

    venus_on_required2 = RequisitionRule(
        logic=Logic(
            predicate=('recorded_hiv_result', 'ne', 'POS'),
            consequence='not_required',
            alternative='none'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Venous (HIV)'],)

    #ELISA is not reuired untill Microtube result is IND. That happens in HivResultReultGroup
    #Next two rules make sure its always NOT_REQUIRED when this form is being fileed.
    elisa_on_required1 = RequisitionRule(
        logic=Logic(
            predicate=('recorded_hiv_result', 'equals', 'IND'),
            consequence='not_required',
            alternative='none'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['ELISA'],)

    elisa_on_required2 = RequisitionRule(
        logic=Logic(
            predicate=('recorded_hiv_result', 'ne', 'IND'),
            consequence='not_required',
            alternative='none'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['ELISA'],)

    rbd_vl_known_pos = RequisitionRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='not_required',
            alternative='new'),
#         helper_class=SubjectStatusRuleHelper,
#         helper_class_attr='hiv_result_required',
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Research Blood Draw', 'Viral Load',])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivTestReview
site_rule_groups.register(ReviewPositiveRuleGroup)


class HivDocumentationGroup(RuleGroup):
    pima_required = ScheduledDataRule(
        logic=Logic(
            predicate=func_pima_required,
            consequence='new',
            alternative='not_required'),
#         helper_class=SubjectStatusRuleHelper,
#         helper_class_attr='pima_required',
        target_model=['pima'])

#    requires Todays HIV results form when the other HIV result documentation form  recorded result is POS
    require_todays_hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='new',
            alternative='not_required'),
        target_model=['hivresult'])

    hic = ScheduledDataRule(
        logic=Logic(
            predicate=func_not_hiv_positive_today,
            consequence='new',
            alternative='not_required'),
        target_model=['hicenrollment'])

    microtube_known_pos = RequisitionRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Microtube'],)

    #Venus is not reuired untill Microtube does not have enoguh volume. That happens in HivResultReultGroup
    #Next two rules make sure its always NOT_REQUIRED when this form is being fileed.
    venus_on_required1 = RequisitionRule(
        logic=Logic(
            predicate=('result_recorded', 'equals', 'POS'),
            consequence='not_required',
            alternative='none'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Venous (HIV)'],)

    venus_on_required2 = RequisitionRule(
        logic=Logic(
            predicate=('result_recorded', 'ne', 'POS'),
            consequence='not_required',
            alternative='none'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Venous (HIV)'],)

    #ELISA is not reuired untill Microtube result is IND. That happens in HivResultReultGroup
    #Next two rules make sure its always NOT_REQUIRED when this form is being fileed.
    elisa_on_required1 = RequisitionRule(
        logic=Logic(
            predicate=('result_recorded', 'equals', 'IND'),
            consequence='not_required',
            alternative='none'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['ELISA'],)

    elisa_on_required2 = RequisitionRule(
        logic=Logic(
            predicate=('result_recorded', 'ne', 'IND'),
            consequence='not_required',
            alternative='none'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['ELISA'],)

    rbd_vl_known_pos = RequisitionRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='not_required',
            alternative='new'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Research Blood Draw', 'Viral Load'])

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

    pima_required = ScheduledDataRule(
        logic=Logic(
            predicate=func_pima_required,
            consequence='new',
            alternative='not_required'),
        target_model=['pima'])

    require_todays_hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='new',
            alternative='not_required'),
        target_model=['hivresult'])

    hic = ScheduledDataRule(
        logic=Logic(
            predicate=func_not_hiv_positive_today,
            consequence='new',
            alternative='not_required'),
        target_model=['hicenrollment'])

    microtube_known_pos = RequisitionRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Microtube'],)

    rbd_vl_known_pos = RequisitionRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='not_required',
            alternative='new'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Research Blood Draw', 'Viral Load'])

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

    tb_record = ScheduledDataRule(
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


class RequisitionRuleGroup(RuleGroup):

    """Ensures an RBD, VL blood draw requisition if HIV result is POS."""
    hiv_result1 = RequisitionRule(
        logic=Logic(
            predicate=func_hiv_positive_today,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Research Blood Draw', 'Viral Load'], )

    """Ensures an ELISA blood draw requisition if HIV result is IND."""
    hiv_result2 = RequisitionRule(
        logic=Logic(
            predicate=func_hiv_indeterminate_today,
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

    pima_required = ScheduledDataRule(
        logic=Logic(
            predicate=func_pima_required,
            consequence='new',
            alternative='not_required'),
        target_model=['pima'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivResult
site_rule_groups.register(RequisitionRuleGroup)

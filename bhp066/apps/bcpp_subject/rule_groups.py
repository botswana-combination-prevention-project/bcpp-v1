from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import RuleGroup, site_rule_groups, ScheduledDataRule, Logic, RequisitionRule

from .classes import SubjectStatusHelper

from .models import (SubjectVisit, ResourceUtilization, HivTestingHistory,
                    SexualBehaviour, HivCareAdherence, Circumcision,
                    HivTestReview, ReproductiveHealth, MedicalDiagnoses,
                    HivResult, HivResultDocumentation, Participation,
                    ElisaHivResult)

from .constants import RBD, Questionnaires


def func_hiv_tested(visit_instance):
    testing_history = HivTestingHistory.objects.get(subject_visit=visit_instance)
    participation = Participation.objects.get(subject_visit=visit_instance)
    return testing_history.has_tested == 'Yes' and participation.participation_type != 'RBD Only'


def func_hiv_untested(visit_instance):
    testing_history = HivTestingHistory.objects.get(subject_visit=visit_instance)
    participation = Participation.objects.get(subject_visit=visit_instance)
    return testing_history.has_tested == 'No' and participation.participation_type != 'RBD Only'


def func_art_naive(visit_instance):
    """Returns True if the participant is NOT on art or cannot be confirmed to be on art"""
    subject_status_helper = SubjectStatusHelper(visit_instance)
    participation = Participation.objects.get(subject_visit=visit_instance)
    return not subject_status_helper.on_art and subject_status_helper.hiv_result == 'POS' and participation.participation_type != 'RBD Only'


def func_known_pos(visit_instance):
    return SubjectStatusHelper(visit_instance).new_pos == False


def func_todays_hiv_result_required(visit_instance):
    """Returns True if the an HIV test is required"""
    subject_status_helper = SubjectStatusHelper(visit_instance)
    participation = Participation.objects.get(subject_visit=visit_instance)
    if participation.participation_type_string == RBD:
        return False
    if participation.participation_type_string == Questionnaires:
        return False
    if subject_status_helper.todays_hiv_result:
        return True
    return False if (subject_status_helper.new_pos == False) else True


def func_hiv_negative_today(visit_instance):
    """Returns True if the participant tests negative today."""
    return SubjectStatusHelper(visit_instance).hiv_result == 'NEG'


def func_hiv_indeterminate_today(visit_instance):
    """Returns True if the participant tests indeterminate today."""
    return SubjectStatusHelper(visit_instance).hiv_result == 'IND'


def func_hiv_positive_today(visit_instance):
    """Returns True if the participant has been determinied to be either known or newly diagnosed HIV positive."""
    return SubjectStatusHelper(visit_instance).hiv_result == 'POS'


def func_hiv_positive_today_not_rbd(visit_instance):
    """Returns True if the participant has been determinied to be either known or newly diagnosed HIV positive
    and their participation is not RBD only."""
    participation = Participation.objects.get(subject_visit=visit_instance)
    return SubjectStatusHelper(visit_instance).hiv_result == 'POS' and participation.participation_type_string != RBD


def func_not_required(visit_instance):
    return True


def func_no_verbal_hiv_result(visit_instance):
    """(('verbal_hiv_result', 'equals', 'IND'), ('verbal_hiv_result', 'equals', 'UNK', 'or'), ('verbal_hiv_result', 'equals', 'not_answering', 'or'))"""
    return SubjectStatusHelper(visit_instance).verbal_hiv_result not in ['POS', 'NEG']


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


class ParticipationRuleGroup(RuleGroup):

    """Makes un-required forms unavailable based on participation"""
    rbd_participation_type = ScheduledDataRule(
        logic=Logic(
            predicate=('participation_type', 'equals', 'RBD Only'),
            consequence='not_required',
            alternative='none'),
        target_model=['communityengagement', 'demographics', 'education', 'hivmedicalcare',
                      'sexualbehaviour', 'monthsrecentpartner', 'monthssecondpartner', 'monthsthirdpartner',
                      'circumcision', 'circumcised', 'uncircumcised', 'reproductivehealth',
                      'pregnancy', 'nonpregnancy', 'medicaldiagnoses', 'heartattack', 'cancer',
                      'sti', 'tubercolosis', 'tbsymptoms', 'substanceuse', 'stigma', 'stigmaopinion',
                      'positiveparticipant', 'accesstocare', 'hivresult', 'elisahivresult',
                      'hicenrollment', 'hivuntested'])

    rbd_requsition = RequisitionRule(
        logic=Logic(
            predicate=('participation_type', 'equals', 'RBD Only'),
            consequence='not_required',
            alternative='none'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Microtube'], )

    htc_participation_type = ScheduledDataRule(
        logic=Logic(
            predicate=('participation_type', 'equals', 'HTC Only'),
            consequence='not_required',
            alternative='none'),
        target_model=['communityengagement', 'demographics', 'education', 'sexualbehaviour',
                      'monthsrecentpartner', 'monthssecondpartner', 'monthsthirdpartner',
                      'circumcision', 'circumcised', 'uncircumcised',
                      'reproductivehealth', 'pregnancy', 'nonpregnancy',
                      'medicaldiagnoses', 'heartattack', 'cancer', 'sti', 'tubercolosis',
                      'tbsymptoms', 'substanceuse', 'stigma', 'stigmaopinion', 'hivmedicalcare'])

    #3forms removed because they assume requisitions have been processed and for questionnaires there are no labs
    questionnaires_participation_type = ScheduledDataRule(
        logic=Logic(
            predicate=('participation_type', 'equals', 'Questionnaires'),
            consequence='not_required',
            alternative='none'),
        target_model=['hivresult', 'elisahivresult', 'pima'])

    questionnaires_requsition = RequisitionRule(
        logic=Logic(
            predicate=('participation_type', 'equals', 'Questionnaires'),
            consequence='not_required',
            alternative='none'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Microtube', 'Venous (HIV)', 'ELISA', 'Viral Load', 'Research Blood Draw'], )

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = Participation
site_rule_groups.register(ParticipationRuleGroup)


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
            #predicate=('has_tested', 'equals', 'Yes'),
            predicate=func_hiv_tested,
            consequence='new',
            alternative='not_required'),
        target_model=['hivtested'])

    hiv_untested = ScheduledDataRule(
        logic=Logic(
            #predicate=('has_tested', 'equals', 'No'),
            predicate=func_hiv_untested,
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

    #added because when participant is -VE, positive participant form was still available
    #and then now after saving hivtestreview, adherence & medicalcare form are available
    verbal_result_response = ScheduledDataRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'equals', 'NEG'),
            consequence='not_required',
            alternative='new'),
        target_model=['positiveparticipant', 'hivcareadherence', 'hivmedicalcare'])

    other_response = ScheduledDataRule(
        logic=Logic(
            predicate=func_no_verbal_hiv_result,
            consequence='not_required',
            alternative='none'),
        target_model=['hivcareadherence', 'hivmedicalcare', 'positiveparticipant', 'stigma', 'stigmaopinion'])

    microtube = RequisitionRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Microtube'],)

    rbd_participation = ScheduledDataRule(
        logic=Logic(
            predicate=('participation_type_string', 'equals', 'RBD'),
            consequence='not_required',
            alternative='none'),
        target_model=['pima', 'positiveparticipant', 'hivcareadherence', 'hivmedicalcare', 'hivtested', 'hivuntested'])

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
            consequence='new',
            alternative='not_required'),
        target_model=['hivcareadherence', 'hivmedicalcare', 'positiveparticipant'])

    recorded_hivresult = ScheduledDataRule(
        logic=Logic(
            predicate=('recorded_hiv_result', 'equals', 'NEG'),
            consequence='new',
            alternative='not_required'),
        target_model=['stigma', 'stigmaopinion'])

    #added to make adherence, medicalcare and positiveparticipant forms unavailable for -ve participants
    recorded_result_response = ScheduledDataRule(
        logic=Logic(
            predicate=('recorded_hiv_result', 'equals', 'NEG'),
            consequence='not_required',
            alternative='new'),
        target_model=['positiveparticipant', 'hivcareadherence', 'hivmedicalcare'])

    require_todays_hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='new',
            alternative='not_required'),
        target_model=['hivresult'])

    microtube = RequisitionRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Microtube'],)

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = HivTestReview
site_rule_groups.register(ReviewPositiveRuleGroup)


# class HivDocumentationGroup(RuleGroup):
# 
#     pima_for_art_naive = ScheduledDataRule(
#         logic=Logic(
#             predicate=func_art_naive,
#             consequence='new',
#             alternative='not_required'),
#         target_model=['pima'])
# 
# #    requires Todays HIV results form when the other HIV result documentation form  recorded result is POS
#     require_todays_hiv_result = ScheduledDataRule(
#         logic=Logic(
#             predicate=func_todays_hiv_result_required,
#             consequence='new',
#             alternative='not_required'),
#         target_model=['hivresult'])
# 
#     microtube = RequisitionRule(
#         logic=Logic(
#             predicate=func_todays_hiv_result_required,
#             consequence='new',
#             alternative='not_required'),
#         target_model=[('bcpp_lab', 'subjectrequisition')],
#         target_requisition_panels=['Microtube'],)
# 
#     #Venus is not reuired untill Microtube does not have enoguh volume. That happens in HivResultReultGroup
#     #Next two rules make sure its always NOT_REQUIRED when this form is being filled.
#     venus_on_required1 = RequisitionRule(
#         logic=Logic(
#             predicate=('result_recorded', 'equals', 'POS'),
#             consequence='not_required',
#             alternative='none'),
#         target_model=[('bcpp_lab', 'subjectrequisition')],
#         target_requisition_panels=['Venous (HIV)'],)
# 
#     venus_on_required2 = RequisitionRule(
#         logic=Logic(
#             predicate=('result_recorded', 'ne', 'POS'),
#             consequence='not_required',
#             alternative='none'),
#         target_model=[('bcpp_lab', 'subjectrequisition')],
#         target_requisition_panels=['Venous (HIV)'],)
# 
#     #ELISA is not reuired untill Microtube result is IND. That happens in HivResultReultGroup
#     #Next two rules make sure its always NOT_REQUIRED when this form is being fileed.
#     elisa_on_required1 = RequisitionRule(
#         logic=Logic(
#             predicate=('result_recorded', 'equals', 'IND'),
#             consequence='not_required',
#             alternative='none'),
#         target_model=[('bcpp_lab', 'subjectrequisition')],
#         target_requisition_panels=['ELISA'],)
# 
#     elisa_on_required2 = RequisitionRule(
#         logic=Logic(
#             predicate=('result_recorded', 'ne', 'IND'),
#             consequence='not_required',
#             alternative='none'),
#         target_model=[('bcpp_lab', 'subjectrequisition')],
#         target_requisition_panels=['ELISA'],)
# 
#     class Meta:
#         app_label = 'bcpp_subject'
#         source_fk = (SubjectVisit, 'subject_visit')
#         source_model = HivResultDocumentation
# site_rule_groups.register(HivDocumentationGroup)


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

    microtube_known_pos = RequisitionRule(
        logic=Logic(
            predicate=func_todays_hiv_result_required,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Microtube'],)

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
            predicate=(('ever_sex', 'equals', 'No'), ('ever_sex', 'equals', 'DWTA', 'or')),
            consequence='not_required',
            alternative='new'),
        target_model=['reproductivehealth', 'pregnancy'])

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
        target_model=['tubercolosis', 'tbsymptoms'])

    class Meta:
        app_label = 'bcpp_subject'
        source_fk = (SubjectVisit, 'subject_visit')
        source_model = MedicalDiagnoses
site_rule_groups.register(MedicalDiagnosesRuleGroup)


class BaseRequisitionRuleGroup(RuleGroup):

    """Ensures an RBD requisition if HIV result is POS."""
    rbd_for_pos = RequisitionRule(
        logic=Logic(
            predicate=func_hiv_positive_today,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Research Blood Draw'], )

    """Ensures an VL requisition if HIV result is POS and participation in NOT RBD only."""
    vl_for_pos = RequisitionRule(
        logic=Logic(
            predicate=func_hiv_positive_today_not_rbd,
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Viral Load'], )

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

    """Ensures a venous blood draw requisition is required if insufficient volume in the capillary (microtube)."""
    venous_for_vol = RequisitionRule(
        logic=Logic(
            predicate=(('insufficient_vol', 'equals', 'Yes'), ('blood_draw_type', 'equals', 'venous', 'or'),),
            consequence='new',
            alternative='not_required'),
        target_model=[('bcpp_lab', 'subjectrequisition')],
        target_requisition_panels=['Venous (HIV)'], )

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

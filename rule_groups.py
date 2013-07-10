from bhp_entry_rules.classes import RuleGroup, rule_groups, ScheduledDataRule, AdditionalDataRule, Logic
from bhp_registration.models import RegisteredSubject
from models import (SubjectVisit, ResourceUtilization, HivTestingHistory, 
                    SexualBehaviour, HivCareAdherence, Circumcision, 
                    HivTestReview, ReproductiveHealth, MedicalDiagnoses)


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
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = ResourceUtilization
rule_groups.register(ResourceUtilizationRuleGroup)


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


    class Meta:
        app_label = 'bcpp_subject'
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = HivTestingHistory
rule_groups.register(HivTestingHistoryRuleGroup)


class SexualBehaviourRuleGroup(RuleGroup):

    ever_sex_two = ScheduledDataRule(
        logic=Logic(
            predicate=(('ever_sex', 'equals', 'No'),('ever_sex', 'equals', 'Don\'t want to answer', 'or')),
            consequence='not_required',
            alternative='new'),
        target_model=['monthsrecentpartner', 'monthssecondpartner', 'monthsthirdpartner'])
    
    partner = ScheduledDataRule(
        logic=Logic(
            predicate=('last_year_partners', 'equals', 0),
            consequence='not_required',
            alternative='new'),
        target_model=['monthsrecentpartner', 'monthssecondpartner', 'monthsthirdpartner'])

    partners = ScheduledDataRule(
        logic=Logic(
            predicate=('last_year_partners', 'equals', 1),
            consequence='not_required',
            alternative='new'),
        target_model=['monthssecondpartner', 'monthsthirdpartner'])
    
    last_year_partners = ScheduledDataRule(
        logic=Logic(
            predicate=('last_year_partners', 'equals', 2),
            consequence='not_required',
            alternative='new'),
        target_model=['monthsthirdpartner'])
    
    more_partners = ScheduledDataRule(
        logic=Logic(
            predicate=('last_year_partners', 'gt', 2),
            consequence='new',
            alternative='not_required'),
        target_model=['monthsrecentpartner', 'monthssecondpartner', 'monthsthirdpartner'])
    
    class Meta:
        app_label = 'bcpp_subject'
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = SexualBehaviour
rule_groups.register(SexualBehaviourRuleGroup)


class MedicalCareRuleGroup(RuleGroup):

    medical_care = ScheduledDataRule(
        logic=Logic(
            predicate=('medical_care', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivmedicalcare'])

    class Meta:
        app_label = 'bcpp_subject'
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = HivCareAdherence
rule_groups.register(MedicalCareRuleGroup)


class MaleCircumcisionRuleGroup(RuleGroup):

    gender = ScheduledDataRule(
        logic=Logic(
            predicate=('gender', 'equals', 'f'),
            consequence='not_required',
            alternative='new'),
        target_model=['circumcision', 'circumcised', 'uncircumcised'])

    class Meta:
        app_label = 'bcpp_subject'
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = RegisteredSubject
rule_groups.register(MaleCircumcisionRuleGroup)


class CircumcisionRuleGroup(RuleGroup):

    circumcised = ScheduledDataRule(
        logic=Logic(
            predicate=('circumcised', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['circumcised'])
    
    circumcised = ScheduledDataRule(
        logic=Logic(
            predicate=('circumcised', 'equals', 'No'),
            consequence='new',
            alternative='not_required'),
        target_model=['uncircumcised'])

    class Meta:
        app_label = 'bcpp_subject'
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = Circumcision
rule_groups.register(CircumcisionRuleGroup)


class FemaleReproductiveRuleGroup(RuleGroup):

    gender = ScheduledDataRule(
        logic=Logic(
            predicate=('gender', 'equals', 'm'),
            consequence='not_required',
            alternative='new'),
        target_model=['reproductivehealth', 'pregnancy'])

    class Meta:
        app_label = 'bcpp_subject'
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = RegisteredSubject
rule_groups.register(FemaleReproductiveRuleGroup)



class ReproductiveRuleGroup(RuleGroup):

    menopause = ScheduledDataRule(
        logic=Logic(
            predicate=('menopause', 'equals', 'No'),
            consequence='new',
            alternative='not_required'),
        target_model=['pregnancy'])

    class Meta:
        app_label = 'bcpp_subject'
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = ReproductiveHealth
rule_groups.register(ReproductiveRuleGroup)



class StigmaPositiveARuleGroup(RuleGroup):

    hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=('hiv_result', 'equals', 'Positive'),
            consequence='new',
            alternative='not_required'),
        target_model=['positiveparticipant', 'hivhealthcarecosts', 'labourmarketwages'])

    HH_hivtest = ScheduledDataRule(
        logic=Logic(
            predicate=('hiv_result', 'equals', 'Negative'),
            consequence='new',
            alternative='not_required'),
        target_model=['futurehivtesting','stigma', 'stigmaopinion'])

    class Meta:
        app_label = 'bcpp_subject'
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = HivTestingHistory
rule_groups.register(StigmaPositiveARuleGroup)


class StigmaPositiveBRuleGroup(RuleGroup):

    recorded_hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=('recorded_hiv_result', 'equals', 'HIV-Positive'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivcareadherence','positiveparticipant', 'hivhealthcarecosts', 'labourmarketwages'])
    
    verbal_hiv_result = ScheduledDataRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'equals', 'HIV-Positive'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivcareadherence', 'positiveparticipant', 'hivhealthcarecosts', 'labourmarketwages'])

    recorded_hivresult = ScheduledDataRule(
        logic=Logic(
            predicate=('recorded_hiv_result', 'equals', 'HIV-Negative'),
            consequence='new',
            alternative='not_required'),
        target_model=['futurehivtesting','stigma', 'stigmaopinion'])

    verbal_hivresult = ScheduledDataRule(
        logic=Logic(
            predicate=('verbal_hiv_result', 'equals', 'HIV-Negative'),
            consequence='new',
            alternative='not_required'),
        target_model=['futurehivtesting','stigma', 'stigmaopinion'])


    class Meta:
        app_label = 'bcpp_subject'
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = HivTestReview
rule_groups.register(StigmaPositiveBRuleGroup)


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
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = MedicalDiagnoses
rule_groups.register(MedicalDiagnosesRuleGroup)


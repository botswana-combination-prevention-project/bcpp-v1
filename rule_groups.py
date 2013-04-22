from bhp_entry_rules.classes import RuleGroup, rule_groups, ScheduledDataRule, AdditionalDataRule, Logic
from bhp_registration.models import RegisteredSubject
from models import SubjectVisit, ResourceUtilization, HivTestingHistory, SexualBehaviour, MonthsRecentPartner, MonthsSecondPartner, HivCareAdherence, Circumcision


class ResourceUtilizationRuleGroup(RuleGroup):

    out_patient = ScheduledDataRule(
        logic=Logic(
            predicate=(('out_patient', 'equals', 'no'), ('out_patient', 'equals', 'REF', 'or')),
            consequence='not_required',
            alternative='new'),
        target_model=['outpatientcare'])

    hospitalized = ScheduledDataRule(
        logic=Logic(
            predicate=(('hospitalized', 'equals', ''), ('hospitalized', 'equals', 0 , 'or')),
            consequence='not_required',
            alternative='new'),
        target_model=['hospitaladmission'])

    class Meta:
        app_label = 'bcpp_subject'
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = ResourceUtilization
rule_groups.register(ResourceUtilizationRuleGroup)


class HivTestingHistoryRuleGroup(RuleGroup):

    hivtestrecord = ScheduledDataRule(
        logic=Logic(
            predicate=('hivtestrecord', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['hivtestreview'])

    class Meta:
        app_label = 'bcpp_subject'
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = HivTestingHistory
rule_groups.register(HivTestingHistoryRuleGroup)


class SexualBehaviourRuleGroup(RuleGroup):
    
    eversex_two = ScheduledDataRule(
        logic=Logic(
            predicate=('eversex', 'equals', 'No'),
            consequence='not_required',
            alternative='new'),
        target_model=['monthsrecentpartner', 'monthssecondpartner', 'monthsthirdpartner'])
    
    eversex = ScheduledDataRule(
        logic=Logic(
            predicate=('eversex', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['monthsrecentpartner'])

    class Meta:
        app_label = 'bcpp_subject'
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = SexualBehaviour
rule_groups.register(SexualBehaviourRuleGroup)


class SexualPartnersRuleGroup(RuleGroup):
    
    concurrent = ScheduledDataRule(
        logic=Logic(
            predicate=('concurrent', 'equals', 'Yes'),
            consequence='not_required',
            alternative='new'),
        target_model=['monthssecondpartner'])
    
    class Meta:
        app_label = 'bcpp_subject'
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = MonthsRecentPartner
rule_groups.register(SexualPartnersRuleGroup)
    

class MoreSexualPartnersRuleGroup(RuleGroup):
    
    concurrent = ScheduledDataRule(
        logic=Logic(
            predicate=('concurrent', 'equals', 'Yes'),
            consequence='not_required',
            alternative='new'),
        target_model=['monthsthirdpartner'])
    
    class Meta:
        app_label = 'bcpp_subject'
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = MonthsSecondPartner
rule_groups.register(MoreSexualPartnersRuleGroup)


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
    
    class Meta:
        app_label = 'bcpp_subject'
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = Circumcision
rule_groups.register(CircumcisionRuleGroup)


class NoCircumcisionRuleGroup(RuleGroup):
    
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
rule_groups.register(NoCircumcisionRuleGroup)


class FemaleReproductiveRuleGroup(RuleGroup):

    gender = ScheduledDataRule(
        logic=Logic(
            predicate=('gender', 'equals', 'm'),
            consequence='not_required',
            alternative='new'),
        target_model=['reproductivehealth'])

    class Meta:
        app_label = 'bcpp_subject'
        filter_model = (SubjectVisit, 'subject_visit')
        source_model = RegisteredSubject
rule_groups.register(FemaleReproductiveRuleGroup)

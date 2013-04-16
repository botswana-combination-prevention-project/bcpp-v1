from bhp_entry_rules.classes import RuleGroup, rule_groups, ScheduledDataRule, AdditionalDataRule, Logic
# from bhp_registration.models import RegisteredSubject
from models import SubjectVisit, ResourceUtilization


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

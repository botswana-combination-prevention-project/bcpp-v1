from bhp_entry_rules.classes import RuleGroup, rule_groups, ScheduledDataRule, AdditionalDataRule, Logic
from bhp_registration.models import RegisteredSubject
from models import HtcVisit, HivTestingHistory


class MaleCircumcisionRuleGroup(RuleGroup):

    gender = ScheduledDataRule(
        logic=Logic(
            predicate=('gender', 'equals', 'f'),
            consequence='not_required',
            alternative='new'),
        target_model=['circumcision'])

    class Meta:
        app_label = 'bcpp_htc'
        filter_model = (HtcVisit, 'htc_visit')
        source_model = RegisteredSubject
rule_groups.register(MaleCircumcisionRuleGroup)


class HivTestingHistoryRuleGroup(RuleGroup):
    
    hiv_record = ScheduledDataRule(
        logic=Logic(
            predicate=('hiv_record', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['lasthivrecord'])
    
    class Meta:
        app_label = 'bcpp_htc'
        filter_model = (HtcVisit, 'htc_visit')
        source_model = HivTestingHistory
rule_groups.register(HivTestingHistoryRuleGroup)

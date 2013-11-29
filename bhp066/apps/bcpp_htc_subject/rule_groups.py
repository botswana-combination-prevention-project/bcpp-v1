from edc.subject.rule_groups.classes import RuleGroup, site_rule_groups, ScheduledDataRule, Logic
from edc.subject.registration.models import RegisteredSubject
from .models import HtcSubjectVisit, HtcHivTestingHistory, HtcHivResult, HivTestingConsent


class GenderRuleGroup(RuleGroup):

    female = ScheduledDataRule(
        logic=Logic(
            predicate=('gender', 'equals', 'f'),
            consequence='not_required',
            alternative='new'),
        target_model=['htccircumcision', 'malefollowup', 'circumcisionappointment'])

    male = ScheduledDataRule(
        logic=Logic(
            predicate=('gender', 'equals', 'm'),
            consequence='not_required',
            alternative='new'),
        target_model=['pregnantfollowup'])

    class Meta:
        app_label = 'bcpp_htc_subject'
        filter_model = (HtcSubjectVisit, 'htc_subject_visit')
        source_model = RegisteredSubject
site_rule_groups.register(GenderRuleGroup)


class HivTestingHistoryRuleGroup(RuleGroup):

    hiv_record = ScheduledDataRule(
        logic=Logic(
            predicate=('hiv_record', 'equals', 'Yes'),
            consequence='new',
            alternative='not_required'),
        target_model=['lasthivrecord'])

    class Meta:
        app_label = 'bcpp_htc_subject'
        filter_model = (HtcSubjectVisit, 'htc_subject_visit')
        source_model = HtcHivTestingHistory
site_rule_groups.register(HivTestingHistoryRuleGroup)


class HivResultRuleGroup(RuleGroup):

    todays_result = ScheduledDataRule(
        logic=Logic(
            predicate=('todays_result', 'equals', 'NEG'),
            consequence='not_required',
            alternative='new'),
        target_model=['Cd4test', 'positivefollowup'])

    class Meta:
        app_label = 'bcpp_htc_subject'
        filter_model = (HtcSubjectVisit, 'htc_subject_visit')
        source_model = HtcHivResult
site_rule_groups.register(HivResultRuleGroup)


class HivTestingConsentRuleGroup(RuleGroup):

    todays_result = ScheduledDataRule(
        logic=Logic(
            predicate=('testing_today', 'equals', 'No'),
            consequence='not_required',
            alternative='new'),
        target_model=['Cd4test', 'positivefollowup', 'pregnantfollowup', 'malefollowup', 'circumcisionappointment'])

    class Meta:
        app_label = 'bcpp_htc_subject'
        filter_model = (HtcSubjectVisit, 'htc_subject_visit')
        source_model = HivTestingConsent
site_rule_groups.register(HivTestingConsentRuleGroup)

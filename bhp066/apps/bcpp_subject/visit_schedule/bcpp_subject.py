from collections import OrderedDict

from django.db.models import get_model

from edc.constants import REQUIRED, NOT_REQUIRED, NOT_ADDITIONAL, ADDITIONAL
from edc.map.classes import site_mappers
from edc.subject.visit_schedule.classes import (VisitScheduleConfiguration, site_visit_schedules,
                                                EntryTuple, MembershipFormTuple, ScheduleGroupTuple,
                                                RequisitionPanelTuple)

from ..models import SubjectConsent
from apps.bcpp_household.constants import BASELINE_SURVEY_SLUG


class BcppSubjectVisitSchedule(VisitScheduleConfiguration):

    name = 'bcpp subject visit schedule'
    app_label = 'bcpp_subject'

    # membership forms
    # (name, model, visible)
    membership_forms = OrderedDict({
        'bcpp-survey': MembershipFormTuple('bcpp-survey', SubjectConsent, True),
        })

    # schedule groups
    # (name, membership_form_name, grouping_key, comment)
    schedule_groups = OrderedDict({
        'group-1': ScheduleGroupTuple('group-1', 'bcpp-survey', None, None),
        })

    # visit_schedule
    # see edc.subject.visit_schedule.models.visit_defintion
    visit_definitions = OrderedDict(
        {'T0': {
            'title': 'Baseline Household Survey',
            'time_point': 0,
            'base_interval': 0,
            'base_interval_unit': 'D',
            'window_lower_bound': 0,
            'window_lower_bound_unit': 'D',
            'window_upper_bound': 0,
            'window_upper_bound_unit': 'D',
            'grouping': None,
            'visit_tracking_model': get_model('bcpp_subject', 'SubjectVisit'),
            'schedule_group': 'group-1',
            'instructions': None,
            'requisitions': (
                # (entry_order app_label model_name requisition_panel_name panel_type aliquot_type_alpha_code
                #   default_entry_status additional)
                RequisitionPanelTuple(10L, u'bcpp_lab', u'subjectrequisition', 'Research Blood Draw', 'TEST', 'WB',
                                      NOT_REQUIRED, NOT_ADDITIONAL),
                RequisitionPanelTuple(20L, u'bcpp_lab', u'subjectrequisition', 'Viral Load', 'TEST', 'WB',
                                      NOT_REQUIRED, NOT_ADDITIONAL),
                RequisitionPanelTuple(30L, u'bcpp_lab', u'subjectrequisition', 'Microtube', 'STORAGE', 'WB',
                                      REQUIRED, NOT_ADDITIONAL),
                RequisitionPanelTuple(30L, u'bcpp_lab', u'subjectrequisition', 'Venous (HIV)', 'TEST', 'WB',
                                      NOT_REQUIRED, NOT_ADDITIONAL),
                RequisitionPanelTuple(30L, u'bcpp_lab', u'subjectrequisition', 'ELISA', 'TEST', 'WB',
                                      NOT_REQUIRED, NOT_ADDITIONAL)
                ),
            'entries': [
                #  order app_label model_name default_entry_status additional
                EntryTuple(10L, u'bcpp_subject', u'subjectlocator', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(20L, u'bcpp_subject', u'residencymobility', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(30L, u'bcpp_subject', u'communityengagement', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(40L, u'bcpp_subject', u'demographics', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(50L, u'bcpp_subject', u'education', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(60L, u'bcpp_subject', u'hivtestinghistory', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(70L, u'bcpp_subject', u'hivtestreview', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(80L, u'bcpp_subject', u'hivresultdocumentation', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(90L, u'bcpp_subject', u'hivtested', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(100L, u'bcpp_subject', u'hivuntested', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(120L, u'bcpp_subject', u'sexualbehaviour', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(130L, u'bcpp_subject', u'monthsrecentpartner', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(140L, u'bcpp_subject', u'monthssecondpartner', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(150L, u'bcpp_subject', u'monthsthirdpartner', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(160L, u'bcpp_subject', u'hivcareadherence', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(170L, u'bcpp_subject', u'hivmedicalcare', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(180L, u'bcpp_subject', u'circumcision', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(190L, u'bcpp_subject', u'circumcised', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(200L, u'bcpp_subject', u'uncircumcised', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(210L, u'bcpp_subject', u'reproductivehealth', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(220L, u'bcpp_subject', u'pregnancy', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(230L, u'bcpp_subject', u'nonpregnancy', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(240L, u'bcpp_subject', u'medicaldiagnoses', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(250L, u'bcpp_subject', u'heartattack', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(260L, u'bcpp_subject', u'cancer', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(270L, u'bcpp_subject', u'sti', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(280L, u'bcpp_subject', u'tubercolosis', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(290L, u'bcpp_subject', u'tbsymptoms', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(300L, u'bcpp_subject', u'substanceuse', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(320L, u'bcpp_subject', u'stigma', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(330L, u'bcpp_subject', u'stigmaopinion', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(340L, u'bcpp_subject', u'positiveparticipant', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(350L, u'bcpp_subject', u'accesstocare', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(360L, u'bcpp_subject', u'hivresult', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(370L, u'bcpp_subject', u'elisahivresult', NOT_REQUIRED, ADDITIONAL),
                EntryTuple(380L, u'bcpp_subject', u'pima', NOT_REQUIRED, ADDITIONAL),
#                 EntryTuple(390L, u'bcpp_subject', u'pimavl', NOT_REQUIRED, ADDITIONAL),
                EntryTuple(400L, u'bcpp_subject', u'subjectreferral', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(410L, u'bcpp_subject', u'hicenrollment', NOT_REQUIRED, ADDITIONAL),
            ]},
         'T1': {
            'title': 'T1 Annual Household Survey',
            'time_point': 1,
            'base_interval': 0,
            'base_interval_unit': 'D',
            'window_lower_bound': 0,
            'window_lower_bound_unit': 'D',
            'window_upper_bound': 0,
            'window_upper_bound_unit': 'D',
            'grouping': None,
            'visit_tracking_model': get_model('bcpp_subject', 'SubjectVisit'),
            'schedule_group': 'group-1',
            'instructions': None,
            'requisitions': (
                # (entry_order app_label model_name requisition_panel_name panel_type aliquot_type_alpha_code
                #   default_entry_status additional)
                RequisitionPanelTuple(10L, u'bcpp_lab', u'subjectrequisition', 'Research Blood Draw', 'TEST', 'WB',
                                      NOT_REQUIRED, NOT_ADDITIONAL),
                RequisitionPanelTuple(20L, u'bcpp_lab', u'subjectrequisition', 'Viral Load', 'TEST', 'WB',
                                      NOT_REQUIRED, NOT_ADDITIONAL),
                RequisitionPanelTuple(30L, u'bcpp_lab', u'subjectrequisition', 'Microtube', 'STORAGE', 'WB',
                                      REQUIRED, NOT_ADDITIONAL),
                RequisitionPanelTuple(30L, u'bcpp_lab', u'subjectrequisition', 'Venous (HIV)', 'TEST', 'WB',
                                      NOT_REQUIRED, NOT_ADDITIONAL),
                RequisitionPanelTuple(30L, u'bcpp_lab', u'subjectrequisition', 'ELISA', 'TEST', 'WB',
                                      NOT_REQUIRED, NOT_ADDITIONAL)
                ),
            'entries': [
                #  order app_label model_name default_entry_status additional
                EntryTuple(10L, u'bcpp_subject', u'residencymobility', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(20L, u'bcpp_subject', u'demographics', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(30L, u'bcpp_subject', u'education', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(40L, u'bcpp_subject', u'hivtestinghistory', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(50L, u'bcpp_subject', u'hivtestreview', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(60L, u'bcpp_subject', u'hivresultdocumentation', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(70L, u'bcpp_subject', u'hivtested', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(80L, u'bcpp_subject', u'hivuntested', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(90L, u'bcpp_subject', u'sexualbehaviour', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(100L, u'bcpp_subject', u'monthsrecentpartner', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(110L, u'bcpp_subject', u'monthssecondpartner', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(120L, u'bcpp_subject', u'monthsthirdpartner', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(130L, u'bcpp_subject', u'hivcareadherence', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(140L, u'bcpp_subject', u'hivmedicalcare', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(150L, u'bcpp_subject', u'circumcision', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(160L, u'bcpp_subject', u'circumcised', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(170L, u'bcpp_subject', u'uncircumcised', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(180L, u'bcpp_subject', u'reproductivehealth', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(190L, u'bcpp_subject', u'pregnancy', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(200L, u'bcpp_subject', u'nonpregnancy', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(210L, u'bcpp_subject', u'medicaldiagnoses', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(220L, u'bcpp_subject', u'heartattack', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(230L, u'bcpp_subject', u'cancer', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(240L, u'bcpp_subject', u'sti', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(250L, u'bcpp_subject', u'tubercolosis', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(260L, u'bcpp_subject', u'tbsymptoms', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(270L, u'bcpp_subject', u'qualityoflife', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(280L, u'bcpp_subject', u'resourceutilization', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(290L, u'bcpp_subject', u'outpatientcare', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(300L, u'bcpp_subject', u'hospitaladmission', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(310L, u'bcpp_subject', u'hivhealthcarecosts', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(320L, u'bcpp_subject', u'labourmarketwages', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(330L, u'bcpp_subject', u'hivresult', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(340L, u'bcpp_subject', u'elisahivresult', NOT_REQUIRED, ADDITIONAL),
                EntryTuple(350L, u'bcpp_subject', u'pima', NOT_REQUIRED, ADDITIONAL),
#                 EntryTuple(360L, u'bcpp_subject', u'pimavl', NOT_REQUIRED, ADDITIONAL),
                EntryTuple(370L, u'bcpp_subject', u'subjectreferral', REQUIRED, NOT_ADDITIONAL),
                EntryTuple(380L, u'bcpp_subject', u'hicenrollment', NOT_REQUIRED, ADDITIONAL),
            ]}
         }
    )

if site_mappers.current_mapper().intervention is False:
    if site_mappers.current_mapper().current_survey_in_settings != BASELINE_SURVEY_SLUG:
        for item in BcppSubjectVisitSchedule.visit_definitions.get('T0').get('entries'):
            if item.model_name in ['tbsymptoms']:
                BcppSubjectVisitSchedule.visit_definitions.get('T0').get('entries').remove(item)

    for item in BcppSubjectVisitSchedule.visit_definitions.get('T1').get('entries'):
        if item.model_name in ['tbsymptoms', 'hivuntested']:
            BcppSubjectVisitSchedule.visit_definitions.get('T1').get('entries').remove(item)

if site_mappers.current_mapper().intervention is True:
    for item in BcppSubjectVisitSchedule.visit_definitions.get('T1').get('entries'):
        if item.model_name in ['hivuntested']:
            BcppSubjectVisitSchedule.visit_definitions.get('T1').get('entries').remove(item)

site_visit_schedules.register(BcppSubjectVisitSchedule)

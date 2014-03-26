from collections import OrderedDict

from edc.subject.visit_schedule.classes import VisitScheduleConfiguration, site_visit_schedules, EntryTuple, MembershipFormTuple, ScheduleGroupTuple, RequisitionPanelTuple
from edc.utils.constants import REQUIRED, NOT_REQUIRED

from ..models import SubjectVisit, SubjectConsent


class BcppSubjectVisitSchedule(VisitScheduleConfiguration):

    name = 'bcpp subject visit schedule'
    app_label = 'bcpp_subject'

    # membership forms
    # (name, model, visible)
    membership_forms = OrderedDict({
        'bcpp-year-1': MembershipFormTuple('bcpp-year-1', SubjectConsent, True),
        })

    # schedule groups
    # (name, membership_form_name, grouping_key, comment)
    schedule_groups = OrderedDict({
        'group-1': ScheduleGroupTuple('group-1', 'bcpp-year-1', None, None),
        })

    # visit_schedule
    # see edc.subject.visit_schedule.models.visit_defintion
    visit_definitions = OrderedDict(
        {'T0': {
            'title': 'T0',
            'time_point': 0,
            'base_interval': 0,
            'base_interval_unit': 'D',
            'window_lower_bound': 0,
            'window_lower_bound_unit': 'D',
            'window_upper_bound': 0,
            'window_upper_bound_unit': 'D',
            'grouping': None,
            'visit_tracking_model': SubjectVisit,
            'schedule_group': 'group-1',
            'instructions': None,
            'requisitions': (
                # (entry_order, app_label, model_name, panel.name, panel.edc_name, panel.panel_type, aliquot_type_alpha_code)
                RequisitionPanelTuple(10L, u'bcpp_lab', u'subjectrequisition', 'Research Blood Draw', 'TEST', 'WB', NOT_REQUIRED),
                RequisitionPanelTuple(20L, u'bcpp_lab', u'subjectrequisition', 'Viral Load', 'TEST', 'WB', NOT_REQUIRED),
                RequisitionPanelTuple(30L, u'bcpp_lab', u'subjectrequisition', 'Microtube', 'STORAGE', 'WB', REQUIRED),
                RequisitionPanelTuple(30L, u'bcpp_lab', u'subjectrequisition', 'Venous (HIV)', 'TEST', 'WB', NOT_REQUIRED),
                RequisitionPanelTuple(30L, u'bcpp_lab', u'subjectrequisition', 'ELISA', 'TEST', 'WB', NOT_REQUIRED)
                ),
            'entries': (
                EntryTuple(10L, u'bcpp_subject', u'participation', REQUIRED),
                EntryTuple(10L, u'bcpp_subject', u'subjectlocator', REQUIRED),
                EntryTuple(20L, u'bcpp_subject', u'residencymobility', REQUIRED),
                EntryTuple(30L, u'bcpp_subject', u'communityengagement', REQUIRED),
                EntryTuple(40L, u'bcpp_subject', u'demographics', REQUIRED),
                EntryTuple(50L, u'bcpp_subject', u'education', REQUIRED),
                EntryTuple(60L, u'bcpp_subject', u'hivtestinghistory', REQUIRED),
                EntryTuple(70L, u'bcpp_subject', u'hivtestreview', REQUIRED),
                EntryTuple(80L, u'bcpp_subject', u'hivresultdocumentation', REQUIRED),
                EntryTuple(90L, u'bcpp_subject', u'hivtested', REQUIRED),
                EntryTuple(100L, u'bcpp_subject', u'hivuntested', REQUIRED),
                EntryTuple(120L, u'bcpp_subject', u'sexualbehaviour', REQUIRED),
                EntryTuple(130L, u'bcpp_subject', u'monthsrecentpartner', REQUIRED),
                EntryTuple(140L, u'bcpp_subject', u'monthssecondpartner', REQUIRED),
                EntryTuple(150L, u'bcpp_subject', u'monthsthirdpartner', REQUIRED),
                EntryTuple(160L, u'bcpp_subject', u'hivcareadherence', REQUIRED),
                EntryTuple(170L, u'bcpp_subject', u'hivmedicalcare', REQUIRED),
                EntryTuple(180L, u'bcpp_subject', u'circumcision', REQUIRED),
                EntryTuple(190L, u'bcpp_subject', u'circumcised', REQUIRED),
                EntryTuple(200L, u'bcpp_subject', u'uncircumcised', REQUIRED),
                EntryTuple(210L, u'bcpp_subject', u'reproductivehealth', REQUIRED),
                EntryTuple(220L, u'bcpp_subject', u'pregnancy', REQUIRED),
                EntryTuple(230L, u'bcpp_subject', u'nonpregnancy', REQUIRED),
                EntryTuple(240L, u'bcpp_subject', u'medicaldiagnoses', REQUIRED),
                EntryTuple(250L, u'bcpp_subject', u'heartattack', REQUIRED),
                EntryTuple(260L, u'bcpp_subject', u'cancer', REQUIRED),
                EntryTuple(270L, u'bcpp_subject', u'sti', REQUIRED),
                EntryTuple(280L, u'bcpp_subject', u'tubercolosis', REQUIRED),
                EntryTuple(290L, u'bcpp_subject', u'tbsymptoms', REQUIRED),
                EntryTuple(300L, u'bcpp_subject', u'substanceuse', REQUIRED),
                EntryTuple(320L, u'bcpp_subject', u'stigma', REQUIRED),
                EntryTuple(330L, u'bcpp_subject', u'stigmaopinion', REQUIRED),
                EntryTuple(340L, u'bcpp_subject', u'positiveparticipant', REQUIRED),
                EntryTuple(350L, u'bcpp_subject', u'accesstocare', REQUIRED),
                EntryTuple(360L, u'bcpp_subject', u'hivresult', REQUIRED),
                EntryTuple(370L, u'bcpp_subject', u'pima', REQUIRED),
                EntryTuple(380L, u'bcpp_subject', u'subjectreferral', REQUIRED),
                EntryTuple(390L, u'bcpp_subject', u'hicenrollment', REQUIRED),
            )}
        }
    )

site_visit_schedules.register(BcppSubjectVisitSchedule)

from collections import OrderedDict

from edc.subject.visit_schedule.classes import VisitScheduleConfiguration, site_visit_schedules, EntryTuple, MembershipFormTuple, ScheduleGroupTuple, RequisitionPanelTuple

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
                RequisitionPanelTuple(10L, u'bcpp_lab', u'subjectrequisition', 'Research Blood Draw', 'TEST', 'WB'),
                RequisitionPanelTuple(20L, u'bcpp_lab', u'subjectrequisition', 'Viral Load', 'TEST', 'WB'),
                RequisitionPanelTuple(30L, u'bcpp_lab', u'subjectrequisition', 'Microtube', 'STORAGE', 'WB'),
                RequisitionPanelTuple(30L, u'bcpp_lab', u'subjectrequisition', 'Venous (HIV)', 'TEST', 'WB'),
                RequisitionPanelTuple(30L, u'bcpp_lab', u'subjectrequisition', 'ELISA', 'TEST', 'WB')
                ),
            'entries': (
                EntryTuple(10L, u'bcpp_subject', u'participation'),
                EntryTuple(10L, u'bcpp_subject', u'subjectlocator'),
                EntryTuple(20L, u'bcpp_subject', u'residencymobility'),
                EntryTuple(30L, u'bcpp_subject', u'communityengagement'),
                EntryTuple(40L, u'bcpp_subject', u'demographics'),
                EntryTuple(50L, u'bcpp_subject', u'education'),
                EntryTuple(60L, u'bcpp_subject', u'hivtestinghistory'),
                EntryTuple(70L, u'bcpp_subject', u'hivtestreview'),
                EntryTuple(80L, u'bcpp_subject', u'hivresultdocumentation'),
                EntryTuple(90L, u'bcpp_subject', u'hivtested'),
                EntryTuple(100L, u'bcpp_subject', u'hivuntested'),
#                 EntryTuple(110L, u'bcpp_subject', u'futurehivtesting'),
                EntryTuple(120L, u'bcpp_subject', u'sexualbehaviour'),
                EntryTuple(130L, u'bcpp_subject', u'monthsrecentpartner'),
                EntryTuple(140L, u'bcpp_subject', u'monthssecondpartner'),
                EntryTuple(150L, u'bcpp_subject', u'monthsthirdpartner'),
                EntryTuple(160L, u'bcpp_subject', u'hivcareadherence'),
                EntryTuple(170L, u'bcpp_subject', u'hivmedicalcare'),
                EntryTuple(180L, u'bcpp_subject', u'circumcision'),
                EntryTuple(190L, u'bcpp_subject', u'circumcised'),
                EntryTuple(200L, u'bcpp_subject', u'uncircumcised'),
                EntryTuple(210L, u'bcpp_subject', u'reproductivehealth'),
                EntryTuple(220L, u'bcpp_subject', u'pregnancy'),
                EntryTuple(230L, u'bcpp_subject', u'nonpregnancy'),
                EntryTuple(240L, u'bcpp_subject', u'medicaldiagnoses'),
                EntryTuple(250L, u'bcpp_subject', u'heartattack'),
                EntryTuple(260L, u'bcpp_subject', u'cancer'),
                EntryTuple(270L, u'bcpp_subject', u'sti'),
                EntryTuple(280L, u'bcpp_subject', u'tubercolosis'),
                EntryTuple(290L, u'bcpp_subject', u'substanceuse'),
                EntryTuple(300L, u'bcpp_subject', u'stigma'),
                EntryTuple(310L, u'bcpp_subject', u'stigmaopinion'),
                EntryTuple(320L, u'bcpp_subject', u'positiveparticipant'),
                EntryTuple(330L, u'bcpp_subject', u'accesstocare'),
                EntryTuple(340L, u'bcpp_subject', u'hivresult'),
                EntryTuple(350L, u'bcpp_subject', u'pima'),
                EntryTuple(360L, u'bcpp_subject', u'subjectreferral'),
                EntryTuple(370L, u'bcpp_subject', u'hicenrollment'),
            )}
        }
    )

site_visit_schedules.register(BcppSubjectVisitSchedule)

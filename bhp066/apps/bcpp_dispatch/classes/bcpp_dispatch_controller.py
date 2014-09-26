import logging

from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import get_model, get_models, get_app, ForeignKey
from edc.base.model.models import BaseListModel
from edc.device.dispatch.classes import DispatchController
from edc.device.dispatch.exceptions import DispatchError
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.subject.registration.models import RegisteredSubject
from apps.bcpp_survey.models import Survey

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BcppDispatchController(DispatchController):

    def __init__(self, using_source, using_destination, dispatch_container_instance, **kwargs):
        dispatch_container_app_label = 'bcpp_household'
        dispatch_container_model_name = 'plot'
        dispatch_container_identifier_attrname = 'plot_identifier'
        kwargs.update({'lab_app_name': 'bcpp_survey_lab'})
        dispatch_url = '/bcpp_survey/dashboard/plot/'
        super(BcppDispatchController, self).__init__(
            using_source,
            using_destination,
            dispatch_container_app_label,
            dispatch_container_model_name,
            dispatch_container_identifier_attrname,
            getattr(dispatch_container_instance, dispatch_container_identifier_attrname),
            dispatch_url,
            **kwargs)

    def get_surveys(self, using=None):
        """Imports the current survey instance on the producer."""
        using = using or self.get_using_source()
        surveys = Survey.objects.using(using).filter(datetime_start__lte=datetime.today())
        if not surveys:
            raise DispatchError('Cannot find any surveys on \'{0}\' starting on or before today\'s date.'.format(self.get_using_source()))
        return surveys

    def get_allowed_base_models(self):
        return [BaseDispatchSyncUuidModel, Survey]

    def get_base_models_for_default_serialization(self):
        return [Survey]

    def pre_dispatch(self, plot, **kwargs):
        """Create household_structures before dispatch, if they don't exist."""
        survey = kwargs.get('survey', None)
        if survey:
            surveys = [survey]
        else:
            surveys = self.get_surveys()
        HouseholdStructure = get_model('bcpp_household', 'householdstructure')
        for survey in surveys:
            for household in plot.get_contained_households():
                if not HouseholdStructure.objects.using(self.get_using_source()).filter(household=household, survey=survey).exists():
                    # create household_structure, signal takes care of adding the members
                    HouseholdStructure.objects.using(self.get_using_source()).create(household=household,
                                                                                     survey=survey,
                                                                                     member_count=0,
                                                                                     note='created on dispatch')

    def dispatch_prep(self, **kwargs):
        """Get a household with the given identifier for dispatch to the specified producer.

        1. Find the household, import as a json object, and save it on the producer
        2. Get the Household Structure for the household, and survey.
        3. Import the structure as a json object save it on the producer
        4. Get all household structure members with the HouseholdStructure and survey
        5. For each member:
                Fetch registered subject and save on producer
        """
        survey = kwargs.get('survey', None)
        if survey:
            surveys = [survey]
        else:
            # if surveys are not dispatched then they must be on the producer already.
            surveys = self.get_surveys(self.get_using_destination())
        plot_identifier = self.get_container_register_instance().container_identifier
        logger.info("Dispatching data for plot {0}".format(plot_identifier))
        Plot = get_model('bcpp_household', 'plot')
        PlotLog = get_model('bcpp_household', 'plotlog')
        PlotLogEntry = get_model('bcpp_household', 'plotlogentry')
        Household = get_model('bcpp_household', 'household')
        HouseholdLog = get_model('bcpp_household', 'householdlog')
        HouseholdLogEntry = get_model('bcpp_household', 'householdlogentry')
        HouseholdStructure = get_model('bcpp_household', 'householdstructure')
        HouseholdMember = get_model('bcpp_household_member', 'householdmember')
        self.dispatch_list_models('bcpp_household')
        self.dispatch_list_models('bcpp_subject')
#         self.dispatch_crypt()
#         self.dispatch_registered_subjects()
        if Plot.objects.using(self.get_using_source()).filter(plot_identifier=plot_identifier).exists():
            plot = Plot.objects.using(self.get_using_source()).get(plot_identifier=plot_identifier)
            if PlotLog.objects.filter(plot=plot).exists():
                plot_log = PlotLog.objects.using(self.get_using_source()).get(plot=plot)
                plot_log_entries = PlotLogEntry.objects.using(self.get_using_source()).filter(plot_log=plot_log)
                self.dispatch_user_items_as_json(plot_log, plot, ['plot_id'])
                if plot_log_entries:
                    self.dispatch_user_items_as_json(plot_log_entries, plot, ['plot_log_id, plot_id'])
            # self.dispatch_user_container_as_json(plot)
            for household in Household.objects.using(self.get_using_source()).filter(plot=plot):
                self.dispatch_user_items_as_json(household, plot, ['plot_id'])
                # for survey in surveys:
                #    self.dispatch_user_items_as_json(survey, plot)
                for survey in surveys:
                    household_structure = HouseholdStructure.objects.filter(household=household, survey_id=survey.id)
                    if household_structure:
                        self.dispatch_user_items_as_json(household_structure, plot, ['plot_id', 'household_id', 'survey_id'])
                        if HouseholdLog.objects.using(self.get_using_source()).filter(household_structure=household_structure).exists():
                            household_logs = HouseholdLog.objects.using(self.get_using_source()).filter(household_structure=household_structure)
                            household_log_entries = HouseholdLogEntry.objects.using(self.get_using_source()).filter(household_log__in=household_logs)
                            self.dispatch_user_items_as_json(household_logs, plot, ['survey_id', 'household_id', 'household_structure_id', 'plot_id'])
                            if household_log_entries:
                                self.dispatch_user_items_as_json(household_log_entries, plot, ['household_log_id'])
                        household_members = HouseholdMember.objects.using(self.get_using_source()).filter(household_structure=household_structure)
                        if household_members:
                            missing_rs = [hsm for hsm in household_members if not hsm.registered_subject]
                            if missing_rs:
                                raise DispatchError('HouseholdMember field registered_subject cannot be None. Got {0}.'.format(missing_rs))
                            registered_subjects = RegisteredSubject.objects.filter(pk__in=[hsm.registered_subject.pk for hsm in household_members])
                            self._dispatch_as_json(
                                registered_subjects,
                                plot,
                                additional_base_model_class=RegisteredSubject,
                                )
                            self.dispatch_user_items_as_json(
                                household_members,
                                plot,
                                ['household_structure_id'],
                                )
                            for household_member in household_members:
                                # dispatch consents
                                # self.dispatch_consent_instances('bcpp_subject', household_member.registered_subject, plot)
                                # dispatch membership forms + consent
                                self.dispatch_membership_forms(
                                    household_member.registered_subject,
                                    plot,
                                    fk_to_skip=['household_member_id', 'survey_id', 'registered_subject_id', 'study_site_id'],
                                    )
                                # dispatch scheduled instances. This will dispatch appointments first
                                self.dispatch_scheduled_instances(
                                    'bcpp_subject',
                                    household_member.registered_subject,
                                    plot,
                                    survey.datetime_start,
                                    survey.datetime_end,
                                    fk_to_skip=['visit_definition_id', 'study_site_id', 'registered_subject_id'],
                                    options={},
                                    )
                                self.dispatch_requisitions('bcpp_lab', household_member.registered_subject, plot)
                                self.dispatch_member_status_instances(
                                    'bcpp_household_member',
                                    household_member.registered_subject,
                                    plot,
                                    options={},
                                    )
                                self.dispatch_lab_tracker_history(
                                    household_member.registered_subject,
                                    group_name='HIV',
                                    )
                                # self.dispatch_entry_buckets(household_member.registered_subject)#PROBLEM dispatch_entry_buckets missing
                                self.dispatch_membership_form_inlines(
                                    'bcpp_household_member',
                                    household_member.registered_subject,
                                    plot,
                                    ['subject_absentee_id', 'subject_undecided_id', 'subject_other_id'],
                                    )

    def dispatch_member_status_instances(self, app_label, registered_subject, user_container, **kwargs):
        """Dispatches all member status for this subject, e.g SubjectAbsentee, SubjectUndecided, ...."""
        member_status_models = self.get_member_status_models(app_label)
        for member_status_cls in member_status_models:
            member_status = member_status_cls.objects.filter(registered_subject=registered_subject)
            if member_status:
                self.dispatch_user_items_as_json(member_status, user_container)

    def get_member_status_models(self, app_label):
        from apps.bcpp_household_member.models import BaseMemberStatusModel
        return self._get_models_by_base('bcpp_household_member', BaseMemberStatusModel)

    def get_inlines(self, app_name):
        _models = []
        if not app_name:
            raise TypeError('Parameter app_name cannot be None.')
        app = get_app(app_name)
        for model_cls in get_models(app):
            if model_cls._meta.object_name.endswith('Entry'):
                _models.append(model_cls)
        return _models

    def dispatch_membership_form_inlines(self, app_name, registered_subject, user_container, fk_to_skip):
        inline_models = self.get_inlines(app_name)
        for model_cls in inline_models:
            for field in model_cls._meta.fields:
                if isinstance(field, (ForeignKey)):
                    main_cls = field.rel.to
                    if not issubclass(main_cls, BaseListModel):
                        if 'registered_subject' in dir(main_cls):
                            try:
                                field_name = field.name
                                d = {}
                                main_cls_instances = main_cls.objects.filter(registered_subject=registered_subject)
                                for instance in main_cls_instances:
                                    d[field_name] = instance.pk
                                    instances = model_cls.objects.filter(**d)
                                    if instances:
                                        self.dispatch_user_items_as_json(instances, user_container, fk_to_skip)
                            except ObjectDoesNotExist:
                                pass

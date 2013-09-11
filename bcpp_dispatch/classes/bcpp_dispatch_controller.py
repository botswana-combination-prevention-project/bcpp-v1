import logging
from bhp_base_model.models import BaseListModel
from datetime import datetime
from django.db.models import get_model, get_models, get_app, ForeignKey
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import signals
from bhp_subject.models import base_subject_get_or_create_registered_subject_on_post_save
from bhp_dispatch.classes import DispatchController
from bhp_dispatch.exceptions import DispatchError
from bhp_dispatch.models import BaseDispatchSyncUuidModel
#from bcpp_subject.models import bcpp_subject_on_post_save 
from bcpp_subject.models import  BaseMemberStatusModel
from bcpp_household_member.models import household_member_on_pre_save, household_member_on_post_save
from bcpp_survey.models import Survey
from bhp_registration.models import RegisteredSubject

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BcppDispatchController(DispatchController):

    def __init__(self, using_source, using_destination, dispatch_container_instance, **kwargs):
        dispatch_container_app_label = 'bcpp_household'
        dispatch_container_model_name = 'household'
        dispatch_container_identifier_attrname = 'household_identifier'
        kwargs.update({'lab_app_name': 'bcpp_survey_lab'})
        dispatch_url = '/bcpp_survey/dashboard/household/'
        super(BcppDispatchController, self).__init__(
            using_source,
            using_destination,
            dispatch_container_app_label,
            dispatch_container_model_name,
            dispatch_container_identifier_attrname,
            getattr(dispatch_container_instance, dispatch_container_identifier_attrname),
            dispatch_url,
            **kwargs)

    def get_surveys(self):
        """Imports the current survey instance on the producer."""
        surveys = Survey.objects.using(self.get_using_source()).filter(datetime_start__lte=datetime.today())
        if not surveys:
            raise DispatchError('Cannot find any surveys on \'{0}\' starting on or before today\'s date.'.format(self.get_using_source()))
        return surveys

    def get_allowed_base_models(self):
        return [BaseDispatchSyncUuidModel, Survey]

    def get_base_models_for_default_serialization(self):
        return [Survey]

    def disconnect_signals(self):
        """Disconnects signals before saving the serialized object in _to_json."""
        signals.pre_save.disconnect(household_member_on_pre_save, weak=False, dispatch_uid="household_member_on_pre_save")
        signals.post_save.disconnect(household_member_on_post_save, weak=False, dispatch_uid="household_member_on_post_save")
        #signals.post_save.disconnect(bcpp_subject_on_post_save, weak=False, dispatch_uid="bcpp_subject_on_post_save")
        signals.post_save.disconnect(base_subject_get_or_create_registered_subject_on_post_save, weak=False, dispatch_uid="base_subject_get_or_create_registered_subject_on_post_save")

    def reconnect_signals(self):
        """Reconnects signals after saving the serialized object in _to_json."""
        #signals.post_save.connect(bcpp_subject_on_post_save, weak=False, dispatch_uid="bcpp_subject_on_post_save")
        signals.post_save.connect(household_member_on_post_save, weak=False, dispatch_uid="household_member_on_post_save")
        signals.pre_save.connect(household_member_on_pre_save, weak=False, dispatch_uid="household_member_on_pre_save")
        signals.post_save.connect(base_subject_get_or_create_registered_subject_on_post_save, weak=False, dispatch_uid="base_subject_get_or_create_registered_subject_on_post_save")

    def pre_dispatch(self, household, **kwargs):
        """Create household_structures before dispatch, if they don't exist."""
        survey = kwargs.get('survey', None)
        if survey:
            surveys = [survey]
        else:
            surveys = self.get_surveys()
        HouseholdStructure = get_model('bcpp_household', 'householdstructure')
        for survey in surveys:
            if not HouseholdStructure.objects.using(self.get_using_source()).filter(household=household, survey=survey).exists():
                # create household_structure, signal takes care of adding the members
                HouseholdStructure.objects.using(self.get_using_source()).create(household=household, survey=survey, member_count=0, note='created on dispatch')

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
            surveys = self.get_surveys()
        household_identifier = self.get_container_register_instance().container_identifier
        logger.info("Dispatching data for household {0}".format(household_identifier))
        Household = get_model('bcpp_household', 'household')
        HouseholdLog = get_model('bcpp_household', 'householdlog')
        HouseholdLogEntry = get_model('bcpp_household', 'householdlogentry')
        HouseholdStructure = get_model('bcpp_household', 'householdstructure')
        HouseholdMember = get_model('bcpp_household_member', 'householdmember')
        SubjectRcc = get_model('bcpp_subject', 'SubjectRcc')
        SubjectRccContactPreference = get_model('bcpp_subject', 'SubjectRccContactPreference')
        #self.dispatch_lab_list_models()
        self.dispatch_list_models('bcpp_household')
        self.dispatch_list_models('bcpp_subject')
        if Household.objects.using(self.get_using_source()).filter(household_identifier=household_identifier).exists():
            household = Household.objects.using(self.get_using_source()).get(household_identifier=household_identifier)
            for survey in surveys:
                household_structure = HouseholdStructure.objects.filter(household=household, survey=survey)
                if household_structure:
                    self.dispatch_user_items_as_json(household_structure, household)
                    if HouseholdLog.objects.using(self.get_using_source()).filter(household_structure=household_structure).exists():
                        household_logs = HouseholdLog.objects.using(self.get_using_source()).filter(household_structure=household_structure)
                        household_log_entries = HouseholdLogEntry.objects.using(self.get_using_source()).filter(household_log__in=household_logs)
                        self.dispatch_user_items_as_json(household_logs, household, ['survey_id', 'household_id'])
                        if household_log_entries:
                            self.dispatch_user_items_as_json(household_log_entries, household)
                    household_members = HouseholdMember.objects.using(self.get_using_source()).filter(household_structure=household_structure)
                    if household_members:
                        missing_rs = [hsm for hsm in household_members if not hsm.registered_subject]
                        if missing_rs:
                            raise DispatchError('HouseholdMember field registered_subject cannot be None. Got {0}.'.format(missing_rs))
                        registered_subjects = RegisteredSubject.objects.filter(pk__in=[hsm.registered_subject.pk for hsm in household_members])
                        self.dispatch_user_items_as_json(registered_subjects, household)
                        self.dispatch_user_items_as_json(household_members, household, ['survey_id'])
                        
                        for household_member in household_members:
                            # dispatch consents
                            self.dispatch_consent_instances('bcpp_subject', household_member.registered_subject, household)
                            # dispatch membership forms
                            self.dispatch_membership_forms(household_member.registered_subject, household)

                            # dispatch scheduled instances. This will dispatch appointments first
                            self.dispatch_scheduled_instances(
                                'bcpp_subject',
                                household_member.registered_subject,
                                household,
                                survey.datetime_start,
                                survey.datetime_end,
                                options={}
                                )
                            self.dispatch_requisitions('bcpp_lab', household_member.registered_subject, household)
                            self.dispatch_member_status_instances(
                                'bcpp_subject',
                                household_member.registered_subject, 
                                household,
                                options={})
                            self.dispatch_lab_tracker_history(household_member.registered_subject, group_name='HIV')
                            self.dispatch_entry_buckets(household_member.registered_subject)
                            self.dispatch_membership_form_inlines('bcpp_subject', household_member.registered_subject, household, ['subject_absentee_id','subject_undecided_id','subject_other_id'])
                            # dispatch misc
#                            self.dispatch_misc_instances([SubjectRcc], household_member.registered_subject, household, query_hint='household_member__registered_subject')
#                            self.dispatch_misc_instances([SubjectRccContactPreference], household_member.registered_subject, household, query_hint='subject_rcc__household_member__registered_subject')


    def dispatch_member_status_instances(self, app_label, registered_subject, user_container, **kwargs):
        """Dispatches all member status for this subject, e.g SubjectAbsentee, SubjectUndecided, ...."""
        member_status_models = self.get_member_status_models(app_label)
        for member_status_cls in member_status_models:
            member_status = member_status_cls.objects.filter(registered_subject=registered_subject)
            if member_status:
                self.dispatch_user_items_as_json(member_status, user_container)

    def get_member_status_models(self, app_label):
        return self._get_models_by_base('bcpp_subject', BaseMemberStatusModel)

    def get_inlines(self, app_name):
        _models = []
        if not app_name:
            raise TypeError('Parameter app_name cannot be None.')
        app = get_app(app_name)
        for model_cls in get_models(app):
            if model_cls._meta.object_name.endswith('Entry'):
                _models.append(model_cls)
        return _models

    def dispatch_membership_form_inlines(self, app_name, registered_subject, household, fk_to_skip):
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
                                        self.dispatch_user_items_as_json(instances, household, fk_to_skip)
                            except ObjectDoesNotExist:
                                pass

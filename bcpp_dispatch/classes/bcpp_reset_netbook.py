import logging
from django.db.models import get_model
from bhp_dispatch.classes import PrepareDevice, DispatchController


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BcppResetNetbook(PrepareDevice):
    def __init__(self, using_source, using_destination, **kwargs):
        app_name = 'bcpp_subject'
        model_name = 'household'
        kwargs.update({'lab_app_name': 'bcpp_survey_lab'})
        identifier_field_name = 'household_identifier'
        dispatch_url = '/bcpp_survey/dashboard/household/'
        self.helper = DispatchController(using_source, using_destination, app_name, model_name, identifier_field_name, dispatch_url,**kwargs)
        super(BcppResetNetbook, self).__init__(using_source, using_destination, **kwargs)

    def post_prepare(self):
        self.update_registered_subjects()
    
    def update_registered_subjects(self):
        logger.info("Updating the registered subject table...")
        self.update_model(('bhp_registration', 'registeredsubject'))    

    def reset_scheduled_labs(self):
        pass

    def pre_prepare(self):
        """We should probably take a snapshot of the database before reseting the netbook
        
        Should also delete all transactions (which should all have been consumed)?
        """
        pass
        
    def reset_scheduled_forms(self):
        """ Deletes all instances of scheduled forms that were dispatched to the device"""
        scheduled_models = self.helper.get_scheduled_models('bcpp_subject')
        if scheduled_models:
            scheduled_models.reverse()
            for scheduled_model in scheduled_models:
                self.reset_model(scheduled_model)
            
    def reset_membership_forms(self):
        """ Deletes all instances of membership forms that were dispatched to the device"""
        for membershipform_model in self.helper.get_membershipform_models():
            self.reset_model(membershipform_model)
    
    def reset(self, **kwargs):
        """Clears all dispatched data needed for an EDC installation.

        Keywords:
            step: if specified skip to the numbered step. default(0)
        """  
        if self.has_outgoing_transactions():
            raise self.exception("Destination has outgoing transactions. Please sync and try again.")

        Household = get_model('bcpp_household', 'household')
        HouseholdStructure = get_model('bcpp_household', 'HouseholdStructure')
        HouseholdMember = get_model('bcpp_household', 'HouseholdMember')
        Appointment = get_model('bhp_appointment', 'Appointment')
        Visit = get_model('bcpp_subject', 'SubjectVisit')
        SubjectRequisition = get_model('bcpp_survey_lab', 'SubjectRequisition')
        inlines = [('bcpp_subject', 'SubjectAbsenteeEntry'), ('bcpp_subject', 'SubjectUndecidedEntry')]
        
        step = int(kwargs.get('step', 0))
        logger.info('Starting at step {0}'.format(step))
        if not step > 1:
            self.timer()
            logger.info("1. Running pre procedures")
            self.pre_prepare()
        if not step > 2:
            self.timer()
            logger.info("2a. Removing all inlines for membership forms")
            self.reset_listed_models(inlines)
            
            logger.info("2b. Removing all membership forms")
            self.reset_membership_forms() 

        if not step > 3:
            self.timer()
            logger.info("3. Removing all scheduled labs")
            self.reset_model(SubjectRequisition)
        if not step > 4:
            self.timer()
            logger.info("4a. Removing all scheduled forms")
            self.reset_scheduled_forms()
            logger.info("4b. Removing all visits")
            self.reset_model(Visit)
            logger.info("4c. Removing all appointment")
            self.reset_model(Appointment)
        if not step > 5:
            self.timer()
            logger.info("5. Removing Household Members")
            self.reset_model(HouseholdMember)
        if not step > 6:
            self.timer()
            logger.info("6. Removing Household Structures")
            self.reset_model(HouseholdStructure)
        if not step > 7:
            self.timer()
            logger.info("7. Removing Household")
            self.reset_model(Household)                        

        if not step > 8:
            self.timer()
            logger.info("8. Running post procedures...")
            self.post_prepare()
        logger.info("Done")
        self.timer(done=True)

import logging
from datetime import datetime
from django.db.models import Model
from bhp_common.utils import td_to_string
from base_prepare_device import BasePrepareDevice


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class PrepareDevice(BasePrepareDevice):

    def __init__(self, using_source, using_destination, **kwargs):
        """
        Args:
            using_source: settings database key for the source.
            using_destination: settings database key for the destination.
        Keywords:
            exception: exception class to use, e.g. CommandError if this is run as a management command. Default(TypeError)
        """
        super(PrepareDevice, self).__init__(using_source, using_destination, **kwargs)
        self.started = None
        self.start_time = None
        self.end_time = None

    def timer(self, done=None):
        if not self.started:
            self.started = datetime.today()
            logger.info('Starting at {0}'.format(self.started))
        self._end_timer()
        self.start_time = datetime.today()
        if done:
            logger.info("processed in {0}".format(td_to_string(datetime.today() - self.started)))

    def _end_timer(self):
        if self.start_time:
            logger.info("    ....processed in {0}".format(td_to_string(datetime.today() - self.start_time)))

    def pre_prepare(self):
        return None

    def post_prepare(self):
        return None

    def prepare(self, **kwargs):
        """Runs for all common data needed for an EDC installation.

        Keywords:
            step: if specified skip to the numbered step. default(0)
        """
        # check for outgoing transactions first
        if self.has_outgoing_transactions():
            raise self.exception("Destination has outgoing transactions. Please sync and try again.")
        step = int(kwargs.get('step', 0))
        logger.info('Starting at step {0}'.format(step))
#        if not step > 1:
#            self.timer()
#            logger.info("1. Running pre procedures")
#            self.pre_prepare()
#        if not step > 2:
#            self.timer()
#            logger.info("2. Updating content_type")
#            self.update_content_type()
#        if not step > 3:
#            self.timer()
#            logger.info("3. Updating auth...")
#            self.update_auth()
#        if not step > 4:
#            self.timer()
#            logger.info("4. Updating api keys...")
#            self.update_model(('tastypie', 'apikey'), base_model_class=Model)
#        if not step > 5:
#            self.timer()
#            logger.info("5. Updating lists...")
#            self.update_list_models()
#        if not step > 6:
#            self.timer()
#            logger.info("6. Updating bhp variables...")
#            self.update_app_models('bhp_variables')
        if not step > 7:
            self.timer()
            logger.info("7. Updating contenttypemap...")
            logger.info('    ...update')
            self.update_app_models('bhp_content_type_map')
            logger.info('    ...resize')
            self.resize_content_type()
            self.update_app_models('bhp_content_type_map')
            logger.info('    ...pop and sync')
            self.sync_content_type_map()
        if not step > 8:
            self.timer()
            logger.info("8. Updating appointment configuration...")
            self.update_model(("bhp_appointment", "Configuration"))
#        if not step > 9:
#            self.timer()
#            logger.info("9. Updating the Crypt table...")
#            self.update_model(('bhp_crypto', 'crypt'))
#        if not step > 10:
#            self.timer()
#            logger.info("10. Updating the visit definitions...")
#            self.update_app_models('bhp_visit')
#        if not step > 11:
#            self.timer()
#            logger.info("11. Updating subject identifiers...")
##            self.update_app_models('bhp_identifier')
#        if not step > 12:
#            self.timer()
#            logger.info("12. Updating registered subjects...")
##            self.update_model(('bhp_registration', 'RegisteredSubject'))
        if not step > 13:
            self.timer()
            logger.info("13. Updating bhp_consent Attached Models...")
            self.update_model(('bhp_consent', 'AttachedModel'))
        if not step > 14:
            self.timer()
            logger.info("14. Updating bhp_consent Consent Catalogues...")
            self.update_model(('bhp_consent', 'ConsentCatalogue'))
#        if not step > 15:
#            self.timer()
#            logger.info("15. Updating lab test code groups from lab_test_code...")
#            self.update_model(('lab_test_code', 'TestCodeGroup'))
#        if not step > 16:
#            self.timer()
#            logger.info("16. Updating lab test codes from lab_test_code...")
#            self.update_model(('lab_test_code', 'TestCode'))
#        if not step > 17:
#            self.timer()
#            logger.info("17. Updating lab aliquot types from lab_aliquot_list...")
#            self.update_model(('lab_aliquot_list', 'AliquotType'))
#        if not step > 18:
#            self.timer()
#            logger.info("18. Updating lab panel models from lab_panel...")
#            self.update_app_models('lab_panel')         
#        if not step > 19:
#            self.timer()
#            logger.info("19. Updating aliquot types from lab_clinic_api...")
#            self.update_model(('lab_clinic_api', 'AliquotType'))
#        if not step > 20:
#            self.timer()
#            logger.info("20. Updating test code groups from lab_clinic_api...")
#            self.update_model(('lab_clinic_api', 'TestCodeGroup'))  
#        if not step > 21:
#            self.timer()
#            logger.info("21. Updating test codes from lab_clinic_api...")
#            self.update_model(('lab_clinic_api', 'TestCode'))
#        if not step > 22:
#            self.timer()
#            logger.info("22. Updating panel from lab_clinic_api...")
#            self.update_model(('lab_clinic_api', 'Panel'))
#        if not step > 23:
#            self.timer()
#            logger.info("23. Updating review from lab_clinic_api...")
#            self.update_model(('lab_clinic_api', 'Review'))
#        if not step > 24:
#            self.timer()
#            logger.info("24. Updating un-scheduled lab entry buckets from bhp_lab_entry...")
#            self.update_model(('bhp_lab_entry', 'UnscheduledLabEntryBucket'))
#        if not step > 25:
#            self.timer()
#            logger.info("25. Updating lab entry from bhp_lab_entry...")
#            self.update_model(('bhp_lab_entry', 'LabEntry'))         
#        if not step > 26:
#            self.timer()
#            logger.info("26. Updating bhp_entry.models.entry...")
#            self.update_model(('bhp_entry', 'entry'))
#        if not step > 27:
#            self.timer()
#            logger.info("27. Updating api keys...")
#            self.update_api_keys()
        if not step > 28:
            self.timer()
            logger.info("28. Running post procedures...")
            self.post_prepare()
        logger.info("Done")
        self.timer(done=True)

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
        step = int(kwargs.get('step', 0))
        logger.info('Starting at step {0}'.format(step))
        if not step > 1:
            self.timer()
            logger.info("1. Running pre procedures")
            self.pre_prepare()
        if not step > 2:
            self.timer()
            logger.info("2. Updating content_type")
            self.update_content_type()
        if not step > 3:
            self.timer()
            logger.info("3. Updating auth...")
            self.update_auth()
        if not step > 4:
            self.timer()
            logger.info("4. Updating api keys...")
            self.update_model(('tastypie', 'apikey'), base_model_class=Model)
        if not step > 5:
            self.timer()
            logger.info("5. Updating lists...")
            self.update_list_models()
        if not step > 6:
            self.timer()
            logger.info("6. Updating bhp variables...")
            self.update_app_models('bhp_variables')
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
        if not step > 9:
            self.timer()
            logger.info("9. Updating the Crypt table...")
            self.update_model(('bhp_crypto', 'crypt'))
        if not step > 10:
            self.timer()
            logger.info("10. Updating the visit definitions...")
            self.update_app_models('bhp_visit')
        if not step > 11:
            self.timer()
            logger.info("11. Updating subject identifiers...")
            self.update_app_models('bhp_identifier')
        if not step > 12:
            self.timer()
            logger.info("12. Updating bhp_entry.models.entry...")
            self.update_model(('bhp_entry', 'entry'))
        if not step > 13:
            self.timer()
            logger.info("13. Updating api keys...")
            self.update_api_keys()
        if not step > 14:
            self.timer()
            logger.info("14. Running post procedures...")
            self.post_prepare()

        logger.info("Done")
        self.timer(done=True)

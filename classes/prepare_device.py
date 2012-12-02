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
        super(PrepareDevice, self).__init(using_source, using_destination, **kwargs)
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

    def prepare(self):

        self.timer()
        logger.info("Running pre procedures")
        self.pre_prepare()

        self.timer()
        logger.info("Updating content_type")
        self.update_content_type()

        self.timer()
        logger.info("Updating auth...")
        self.update_auth()

        self.timer()
        logger.info("Updating api keys...")
        self.update_model(('tastypie', 'apikey'), base_model_class=Model)

        self.timer()
        logger.info("Updating lists...")
        self.update_list_models()

        self.timer()
        logger.info("Updating bhp variables...")
        self.update_app_models('bhp_variables')

        self.timer()
        logger.info("Updating contenttypemap...")
        logger.info('    ...resize')
        self.resize_content_type()
        logger.info('    ...update')
        self.update_app_models('bhp_content_type_map')
        logger.info('    ...pop and sync')
        self.sync_content_type_map()

        self.timer()
        logger.info("Updating appointment configuration...")
        self.update_model(("bhp_appointment", "Configuration"))

        self.timer()
        logger.info("Updating the Crypt table...")
        self.update_model(('bhp_crypto', 'crypt'))

        self.timer()
        logger.info("Updating the visit definitions...")
        self.update_app_models('bhp_visit')

        self.timer()
        logger.info("Updating subject identifiers...")
        self.update_app_models('bhp_identifier')

        self.timer()
        logger.info("Updating bhp_entry.models.entry...")
        self.update_model(('bhp_entry', 'entry'))

        self.timer()
        logger.info("Updating api keys...")
        self.update_api_keys()

        self.timer()
        logger.info("Running post procedures...")
        self.post_prepare()

        logger.info("Done")
        self.timer(done=True)

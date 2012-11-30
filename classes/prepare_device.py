import logging
import itertools
from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Model
from django.conf import settings
from edc_device_prep import EdcDevicePrep
from bhp_common.utils import td_to_string
from bhp_sync.models import Producer
from bhp_content_type_map.models import ContentTypeMap

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class PrepareDevice(object):

    def __init__(self, using_source, using_destination, **kwargs):
        """
        Args:
            using_source: settings database key for the source.
            using_destination: settings database key for the destination.
        Keywords:
            exception: exception class to use, e.g. CommandError if this is run as a management command. Default(TypeError)
        """
        destination = None
        source = 'default'
        self.exception = kwargs.get('exception', TypeError)
        self.edc_device_prep = EdcDevicePrep()
        if settings.DEVICE_ID == '99':
            # We are on the server
            if destination:
                active_producers = Producer.objects.filter(is_active=True).values_list('name')
                active_producers_lst = list(itertools.chain(*active_producers))
                if not destination in active_producers_lst:
                    raise self.exception("Destination {0} does not match any of the our active producers".format(destination))
            else:
                raise self.exception("Please enter a device name!\n Usage:\n python manage.py prepare_netbook [device_name]")
        else:
            # We are running this on a netbook
            from bhp_sync.classes import TransactionProducer
            destination = 'default'  # str(TransactionProducer())
            source = 'server'

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
            logger.info("........processed in {0}".format(td_to_string(datetime.today() - self.start_time)))

    def pre_prepare(self, source, destination):
        return None

    def post_prepare(self, source, destination):
        return None

    def prepare(self, source, destination):

        self.timer()
        logger.info("....Running pre procedures")
        self.pre_prepare(source, destination)

        self.timer()
        logger.info("....Updating content_type")
        self.edc_device_prep.update_content_type(source, destination)

        self.timer()
        logger.info("....Updating auth")
        self.edc_device_prep.update_auth(source, destination)

        self.timer()
        logger.info("....Updating api keys")
        self.edc_device_prep.update_model(('tastypie', 'apikey'), source, destination, base_model_class=Model)

        self.timer()
        logger.info("....Updating lists")
        self.edc_device_prep.update_list_models(source, destination)

        self.timer()
        logger.info("....Updating bhp variables")
        self.edc_device_prep.update_app_models('bhp_variables', source, destination)

        self.timer()
        logger.info("....Updating contenttypemap")
        logger.info('.......resize')
        self.edc_device_prep.resize_content_type(source, destination)
        logger.info('.......update')
        self.edc_device_prep.update_app_models('bhp_content_type_map', source, destination)
        logger.info('.......pop and sync')
        ContentTypeMap.objects.sync()

        self.timer()
        logger.info('Populating / re-populating from django content type...')

        self.timer()
        logger.info("....Updating survey instances")
        self.edc_device_prep.update_model(('mochudi_survey', 'survey'), source, destination)

        self.timer()
        logger.info("....Updating appointment configuration")
        self.edc_device_prep.update_model(("bhp_appointment", "Configuration"), source, destination)

        self.timer()
        logger.info("....Updating the crypt table")
        self.edc_device_prep.update_model(('bhp_crypto', 'crypt'), source, destination)

        self.timer()
        logger.info("....Updating the visit definitions")
        self.edc_device_prep.update_app_models('bhp_visit', source, destination)

        self.timer()
        logger.info("....Updating subject identifiers")
        self.edc_device_prep.update_app_models('bhp_identifier', source, destination)

        self.timer()
        logger.info("....Updating bhp_entry.models.entry")
        self.edc_device_prep.update_model(('bhp_entry', 'entry'), source, destination)

        self.timer()
        logger.info("....Updating api keys")
        self.edc_device_prep.update_api_keys(source, destination)

        self.timer()
        logger.info("....Running post procedures")
        self.post_prepare(source, destination)

        logger.info("Done")
        self.timer(done=True)

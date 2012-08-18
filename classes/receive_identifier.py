import logging
from datetime import date
from django.conf import settings
from bhp_identifier.classes import BaseIdentifier


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class ReceiveIdentifier(BaseIdentifier):
    """ Sets and returns a receive identifier of format {lab_code}{date_prefix}{sequence} where lab_code is the value of settings.LIS_FACILITY_CODE."""
    def get_identifier_prep(self, **kwargs):
        options = {}
        if 'LIS_FACILITY_CODE' in dir(settings):
            lab_code = settings.LIS_FACILITY_CODE
            logger.warning('Warning: settings attribute LIS_FACILITY_CODE not found, setting to blank.')
        else:
            lab_code = ''
        if 'LIS_MAX_SPECIMENS_PER_MONTH' in dir(settings):
            max_specimens = settings.LIS_MAX_SPECIMENS_PER_MONTH
            logger.warning('Warning: settings attribute LIS_MAX_SPECIMENS_PER_MONTH not found, setting to 100,000.')
        else:
            max_specimens = 100000
        options.update(
            app_name='lab_receive',
            model_name='receiveidentifier',
            padding=int(len(str(max_specimens)) - 1),
            identifier_format='{lab_code}{date_prefix}{{sequence}}'.format(lab_code=lab_code, date_prefix=date.today().strftime('%y%m')))
        return options

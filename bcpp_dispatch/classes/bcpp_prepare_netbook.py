import logging
from edc_lib.bhp_base_model.models import BaseUuidModel, BaseModel
from edc_lib.bhp_dispatch.classes import PrepareDevice


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BcppPrepareNetbook(PrepareDevice):

    def post_prepare(self):
        self.timer()
        logger.info("Updating bcpp_survey.survey instances...")
        self.update_model(('bcpp_survey', 'survey'), [BaseUuidModel])
        self.update_model(('bcpp_household', 'community'), [BaseModel])

    def pre_prepare(self):
        pass

from bhp_base_model.tests.factories import BaseListModelFactory
from bhp_adverse.models import DeathCauseInfo


class DeathCauseInfoFactory(BaseListModelFactory):
    FACTORY_FOR = DeathCauseInfo

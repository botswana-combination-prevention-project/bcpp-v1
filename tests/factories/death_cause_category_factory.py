from bhp_base_model.tests.factories import BaseListModelFactory
from bhp_adverse.models import DeathCauseCategory


class DeathCauseCategoryFactory(BaseListModelFactory):
    FACTORY_FOR = DeathCauseCategory

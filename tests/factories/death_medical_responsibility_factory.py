from bhp_base_model.tests.factories import BaseListModelFactory
from bhp_adverse.models import DeathMedicalResponsibility


class DeathMedicalResponsibilityFactory(BaseListModelFactory):
    FACTORY_FOR = DeathMedicalResponsibility

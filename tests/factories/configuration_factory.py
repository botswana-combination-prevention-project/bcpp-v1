import factory
from datetime import datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_appointment.models import Configuration


class ConfigurationFactory(BaseUuidModelFactory):
    FACTORY_FOR = Configuration

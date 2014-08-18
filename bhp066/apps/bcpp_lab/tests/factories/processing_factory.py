from datetime import datetime
import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import AliquotProcessing
from .aliquot_factory import AliquotFactory
from .profile_factory import ProfileFactory


class ProcessingFactory(BaseUuidModelFactory):
    FACTORY_FOR = AliquotProcessing

    profile = factory.SubFactory(ProfileFactory)
    aliquot = factory.SubFactory(AliquotFactory)
from datetime import datetime
import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import ProfileItem
from .aliquot_type_factory import AliquotTypeFactory
from .profile_factory import ProfileFactory


class ProfileItemFactory(BaseUuidModelFactory):
    FACTORY_FOR = ProfileItem

    profile = factory.SubFactory(ProfileFactory)
    aliquot_type = factory.SubFactory(AliquotTypeFactory)
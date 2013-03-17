import factory
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_variables.models import StudySite


class StudySiteFactory(BaseUuidModelFactory):
    FACTORY_FOR = StudySite

    site_code = factory.Sequence(lambda n: '{0}'.format(n))
    site_name = factory.LazyAttribute(lambda o: 'Site {0}'.format(o.site_code))

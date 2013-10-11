import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import ReproductiveHealth


class ReproductiveHealthFactory(BaseUuidModelFactory):
    FACTORY_FOR = ReproductiveHealth

    report_datetime = datetime.today()
    number_children = 2
    menopause = (('Yes', u'Yes'), ('No', u'No'))[0][0]
    family_planning_other = factory.Sequence(lambda n: 'family_planning_other{0}'.format(n))

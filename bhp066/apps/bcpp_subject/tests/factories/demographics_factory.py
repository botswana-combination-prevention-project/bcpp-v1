import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import Demographics


class DemographicsFactory(BaseUuidModelFactory):
    FACTORY_FOR = Demographics

    report_datetime = datetime.today()
    religion_other = factory.Sequence(lambda n: 'religion_other{0}'.format(n))
    other = factory.Sequence(lambda n: 'other{0}'.format(n))
    marital_status = (('Single/never married', u'Single/never married'), ('Married', u'Married (common law/civil or customary/traditional)'), ('Divorced/separated', u'Divorced or formally separated'), ('Widowed', u'Widowed'), ('not_answering', u"Don't want to answer"))[0][0]

import factory

from datetime import datetime

from ...models import HivTested


class HivTestedFactory(factory.DjangoModelFactory):
    FACTORY_FOR = HivTested

    report_datetime = datetime.today()
    where_hiv_test = (('Tebelopele VCT center', u'Tebelopele VCT center'), ('Antenatal care at healthcare facility', u'Antenatal care at healthcare facility (including private clinics)'), ('Other (not antenatal care) at healthcare facility', u'Other (not antenatal care) at healthcare facility (including private clinics)'), ('In my house as part of door-to-door services', u'In my house as part of door-to-door services'), ('In a mobile tent or vehicle in my neighborhood', u'In a mobile tent or vehicle in my neighborhood'), ('OTHER', u'Other, specify:'), ('not_sure', u'I am not sure'), ('not_answering', u"Don't want to answer"))[0][0]
    where_hiv_test_other = factory.Sequence(lambda n: 'where_hiv_test_other{0}'.format(n))

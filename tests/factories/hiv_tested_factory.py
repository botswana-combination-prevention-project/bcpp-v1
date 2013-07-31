import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import HivTested


class HivTestedFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivTested

    report_datetime = datetime.today()
    where_hiv_test = (('Tebelopele VCT center', u'Tebelopele VCT center'), ('Antenatal care at healthcare facility', u'Antenatal care at healthcare facility (including private clinics)'), ('Other (not antenatal care) at healthcare facility', u'Other (not antenatal care) at healthcare facility (including private clinics)'), ('In my house as part of door-to-door services', u'In my house as part of door-to-door services'), ('In a mobile tent or vehicle in my neighborhood', u'In a mobile tent or vehicle in my neighborhood'), ('Other, specify:', u'Other, specify:'), ('I am not sure', u'I am not sure'), ("Don't want to answer", u"Don't want to answer"))[0][0]

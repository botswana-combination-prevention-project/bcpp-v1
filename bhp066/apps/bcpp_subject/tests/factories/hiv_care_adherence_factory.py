import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import HivCareAdherence


class HivCareAdherenceFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivCareAdherence

    report_datetime = datetime.today()
    medical_care = (('Yes', u'Yes'), ('No', u'No'), ('not_answering', u"Don't want to answer"))[0][0]
    arv_naive = (('Yes', u'Yes'), ('No', u'No'), ('not_answering', u"Don't want to answer"))[0][0]
    why_no_arv_other = factory.Sequence(lambda n: 'why_no_arv_other{0}'.format(n))
    on_arv = (('Yes', u'Yes'), ('No', u'No'), ('not_answering', u"Don't want to answer"))[0][0]
    arv_stop_other = factory.Sequence(lambda n: 'arv_stop_other{0}'.format(n))

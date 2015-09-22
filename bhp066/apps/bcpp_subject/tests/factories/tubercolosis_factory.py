import factory
from datetime import date, datetime
from ...models import Tubercolosis


class TubercolosisFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Tubercolosis

    report_datetime = datetime.today()
    date_tb = date.today()
    dx_tb = (('Pulmonary tuberculosis', u'Pulmonary tuberculosis'), ('Extrapulmonary (outside the lungs) tuberculosis', u'Extrapulmonary (outside the lungs) tuberculosis'), ('Other', u'Other, specify:'), ('not_answering', u"Don't want to answer"))[0][0]

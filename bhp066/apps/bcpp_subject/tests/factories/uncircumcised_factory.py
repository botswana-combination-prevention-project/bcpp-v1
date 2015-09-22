import factory

from datetime import date, datetime

from ...models import Uncircumcised


class UncircumcisedFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Uncircumcised

    report_datetime = datetime.today()
    future_circ = (('Yes', u'Yes'), ('No', u'No'), ('not_sure', u'I am not sure'), ('not_answering', u"Don't want to answer"))[0][0]

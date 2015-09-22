import factory

from datetime import date, datetime

from ...models import NonPregnancy


class NonPregnancyFactory(factory.DjangoModelFactory):
    FACTORY_FOR = NonPregnancy

    report_datetime = datetime.today()
    more_children = (('Yes', u'Yes'), ('No', u'No'), ('not_sure', u'I am not sure'), ('not_answering', u"Don't want to answer"))[0][0]

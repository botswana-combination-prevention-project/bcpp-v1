import factory

from datetime import datetime

from ...models import SexualBehaviour


class SexualBehaviourFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SexualBehaviour

    report_datetime = datetime.today()
    ever_sex = (('Yes', u'Yes'), ('No', u'No'), ('not_answering', u"Don't want to answer"))[0][0]

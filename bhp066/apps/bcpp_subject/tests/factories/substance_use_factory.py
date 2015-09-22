import factory
from datetime import date, datetime
from ...models import SubstanceUse


class SubstanceUseFactory(factory.DjangoModelFactory):
    FACTORY_FOR = SubstanceUse

    report_datetime = datetime.today()
    alcohol = (('Never', u'Never'), ('Less then once a week', u'Less then once a week'), ('Once a week', u'Once a week'), ('2 to 3 times a week', u'2 to 3 times a week'), ('more than 3 times a week', u'more than 3 times a week'), ('not_answering', u"Don't want to answer"))[0][0]
    smoke = (('Yes', u'Yes'), ('No', u'No'), ('not_answering', u"Don't want to answer"))[0][0]

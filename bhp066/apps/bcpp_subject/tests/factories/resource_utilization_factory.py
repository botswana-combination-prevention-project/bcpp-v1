import factory

from datetime import datetime

from ...models import ResourceUtilization


class ResourceUtilizationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ResourceUtilization

    report_datetime = datetime.today()
    out_patient = (('Yes', u'Yes'), ('No', u'No'), ('Refuse', u'Refused to answer'))[0][0]
    money_spent = 2.5
    medical_cover = (('Yes', u'Yes'), ('No', u'No'), ('Refuse', u'Refused to answer'))[0][0]

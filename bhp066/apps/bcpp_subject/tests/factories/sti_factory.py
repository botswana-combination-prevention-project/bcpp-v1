import factory

from datetime import date, datetime

from ...models import Sti


class StiFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Sti

    report_datetime = datetime.today()
    sti_date = date.today()
    sti_dx = (('wasting', u'Severe weight loss (wasting) - more than 10% of body weight'), ('diarrhoea', u'Unexplained diarrhoea for one month'), ('yeast infection', u'Yeast infection of mouth or oesophagus'), ('pneumonia', u'Severe pneumonia or meningitis or sepsis'), ('PCP', u'PCP (Pneumocystis pneumonia)'), ('herpes', u'Herpes infection for more than one month'), ('OTHER', u'Other'))[0][0]

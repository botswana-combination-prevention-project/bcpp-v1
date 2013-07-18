import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import Sti


class StiFactory(BaseUuidModelFactory):
    FACTORY_FOR = Sti

    report_datetime = datetime.today()
    sti_date = date.today()
    sti_dx = (('wasting', 'Severe weight loss (wasting) - more than 10% of body weight'), ('diarrhoea', 'Unexplained diarrhoea for one month'), ('yeast infection', 'Yeast infection of mouth or oesophagus'), ('pneumonia', 'Severe pneumonia or meningitis or sepsis'), ('PCP', 'PCP (Pneumocystis pneumonia)'), ('herpes', 'Herpes infection for more than one month'), ('OTHER', 'Other'))[0][0]

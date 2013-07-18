import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import Demographics


class DemographicsFactory(BaseUuidModelFactory):
    FACTORY_FOR = Demographics

    report_datetime = datetime.today()
    religion_other = factory.Sequence(lambda n: 'religion_other{0}'.format(n))
    ethnic = (('Babirwa', 'Babirwa'), ('Bahambukushu', 'Bahambukushu'), ('Baherero', 'Baherero'), ('Bahurutshe', 'Bahurutshe'), ('Bakalaka', 'Bakalaka'), ('Bakgatla', 'Bakgatla'), ('Bakwena', 'Bakwena'), ('Balete', 'Balete'), ('Bangwaketse', 'Bangwaketse'), ('Bangwato', 'Bangwato'), ('Bakgalagadi', 'Bakgalagadi'), ('Basarwa', 'Basarwa'), ('Basobea', 'Basobea'), ('Batawana', 'Batawana'), ('Batlokwa', 'Batlokwa'), ('Batswapong', 'Batswapong'), ('White African', 'White African'), ('Indian African', 'Indian African'), ('Asian', 'Asian'), ('Other, specify:', 'Other, specify:'), ("Don't want to answer", "Don't want to answer"))[0][0]
    other = factory.Sequence(lambda n: 'other{0}'.format(n))
    marital_status = (('Single/never married', 'Single/never married'), ('Married', 'Married (common law/civil or customary/traditional)'), ('Divorced/separated', 'Divorced or formally separated'), ('Widowed', 'Widowed'), ("Don't want to answer", "Don't want to answer"))[0][0]

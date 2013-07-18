import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import SubstanceUse


class SubstanceUseFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubstanceUse

    report_datetime = datetime.today()
    alcohol = (('Never', 'Never'), ('Less then once a week', 'Less then once a week'), ('Once a week', 'Once a week'), ('2 to 3 times a week', '2 to 3 times a week'), ('more than 3 times a week', 'more than 3 times a week'), ("Don't want to answer", "Don't want to answer"))[0][0]
    smoke = (('Yes', 'Yes'), ('No', 'No'), ("Don't want to answer", "Don't want to answer"))[0][0]

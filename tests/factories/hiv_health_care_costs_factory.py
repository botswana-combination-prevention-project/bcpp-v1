import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import HivHealthCareCosts


class HivHealthCareCostsFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivHealthCareCosts

    report_datetime = datetime.today()
    hiv_medical_care = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    place_care_received = (('Government dispensary', 'Government dispensary'), ('Government health center', 'Government health center'), ('Government hospital', 'Government hospital'), ('Christian/mission health center', 'Christian/mission health center'), ('Islamic health center', 'Islamic health center'), ('Private health center for all illnesses', 'Private health center for all illnesses'), ('Private health center for HIV/AIDS', 'Private health center for HIV/AIDS'), ('Mobile services', 'Mobile services'), ('Plantation health center', 'Plantation health center'), ('NGO clinic', 'NGO clinic'), ("Don't want to answer", "Don't want to answer"))[0][0]
    care_regularity = (('0 times', '0 times'), ('1 time', '1 time'), ('2 times', '2 times'), ('3 times', '3 times'), ('4 times', '4 times'), ('5 times', '5 times'), ('6-10 times', '6-10 times'), ('More than 10 times', 'More than 10 times'), ("Don't want to answer", "Don't want to answer"))[0][0]
    doctor_visits = (('always', 'All of the time (always)'), ('almost always', 'Most of the time (almost always)'), ('sometimes', 'Some of the time (sometimes)'), ('rarely', 'Almost none of the time (rarely)'), ('never', 'None of the time (never)'), ("Don't want to answer", "Don't want to answer"))[0][0]

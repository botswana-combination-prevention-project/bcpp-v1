import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import HivHealthCareCosts


class HivHealthCareCostsFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivHealthCareCosts

    report_datetime = datetime.today()
    hiv_medical_care = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    place_care_received = (('Government dispensary', <django.utils.functional.__proxy__ object at 0x103a1acd0>), ('Government health center', <django.utils.functional.__proxy__ object at 0x103a1ad50>), ('Government hospital', <django.utils.functional.__proxy__ object at 0x103a1add0>), ('Christian/mission health center', <django.utils.functional.__proxy__ object at 0x103a1ae50>), ('Islamic health center', <django.utils.functional.__proxy__ object at 0x103a1aed0>), ('Private health center for all illnesses', <django.utils.functional.__proxy__ object at 0x103a1af50>), ('Private health center for HIV/AIDS', <django.utils.functional.__proxy__ object at 0x103a1afd0>), ('Mobile services', <django.utils.functional.__proxy__ object at 0x103a1c090>), ('Plantation health center', <django.utils.functional.__proxy__ object at 0x103a1c110>), ('NGO clinic', <django.utils.functional.__proxy__ object at 0x103a1c190>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103a1c210>))[0][0]
    care_regularity = (('0 times', <django.utils.functional.__proxy__ object at 0x103a1c290>), ('1 time', <django.utils.functional.__proxy__ object at 0x103a1c310>), ('2 times', <django.utils.functional.__proxy__ object at 0x103a1c390>), ('3 times', <django.utils.functional.__proxy__ object at 0x103a1c410>), ('4 times', <django.utils.functional.__proxy__ object at 0x103a1c490>), ('5 times', <django.utils.functional.__proxy__ object at 0x103a1c510>), ('6-10 times', <django.utils.functional.__proxy__ object at 0x103a1c590>), ('More than 10 times', <django.utils.functional.__proxy__ object at 0x103a1c610>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103a1c690>))[0][0]
    doctor_visits = (('always', <django.utils.functional.__proxy__ object at 0x103a1c710>), ('almost always', <django.utils.functional.__proxy__ object at 0x103a1c790>), ('sometimes', <django.utils.functional.__proxy__ object at 0x103a1c810>), ('rarely', <django.utils.functional.__proxy__ object at 0x103a1c890>), ('never', <django.utils.functional.__proxy__ object at 0x103a1c910>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103a1c990>))[0][0]

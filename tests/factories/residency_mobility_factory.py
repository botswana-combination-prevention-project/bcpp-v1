import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import ResidencyMobility


class ResidencyMobilityFactory(BaseUuidModelFactory):
    FACTORY_FOR = ResidencyMobility

    report_datetime = datetime.today()
    length_residence = (('Less than 6 months', <django.utils.functional.__proxy__ object at 0x103ae4490>), ('6 months to 12 months', <django.utils.functional.__proxy__ object at 0x103ae4510>), ('1 to 5 years', <django.utils.functional.__proxy__ object at 0x103ae4590>), ('More than 5 years', <django.utils.functional.__proxy__ object at 0x103ae4610>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae4690>))[0][0]
    forteen_nights = (('Yes', <django.utils.functional.__proxy__ object at 0x103ae2a10>), ('No', <django.utils.functional.__proxy__ object at 0x103ae2ad0>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae2b50>))[0][0]
    intend_residency = (('Yes', <django.utils.functional.__proxy__ object at 0x103ae2bd0>), ('No', <django.utils.functional.__proxy__ object at 0x103ae2c50>), ('not sure', <django.utils.functional.__proxy__ object at 0x103ae2cd0>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae2d50>))[0][0]
    nights_away = (('zero', <django.utils.functional.__proxy__ object at 0x103ae4710>), ('1-6 nights', <django.utils.functional.__proxy__ object at 0x103ae4790>), ('1-2 weeks', <django.utils.functional.__proxy__ object at 0x103ae4810>), ('3 weeks to less than 1 month', <django.utils.functional.__proxy__ object at 0x103ae4890>), ('1-3 months', <django.utils.functional.__proxy__ object at 0x103ae4910>), ('4-6 months', <django.utils.functional.__proxy__ object at 0x103ae4990>), ('more than 6 months', <django.utils.functional.__proxy__ object at 0x103ae4a10>), ('I am not sure', <django.utils.functional.__proxy__ object at 0x103ae4a90>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae4b10>))[0][0]
    cattle_postlands = (('N/A', <django.utils.functional.__proxy__ object at 0x103ae4b90>), ('Farm/lands', <django.utils.functional.__proxy__ object at 0x103ae4c10>), ('Cattle post', <django.utils.functional.__proxy__ object at 0x103ae4c90>), ('Other community', <django.utils.functional.__proxy__ object at 0x103ae4d10>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae4d90>))[0][0]

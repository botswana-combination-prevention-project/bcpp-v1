import factory
from datetime import datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_household.models import Household


class HouseholdFactory(BaseUuidModelFactory):
    FACTORY_FOR = Household

    household_identifier = factory.Sequence(lambda n: 'H'.format(n.rjust(6, '0')))
    hh_int = factory.Sequence(lambda n: n)
    #gps_device = factory.SubFactory(GpsDeviceFactory)
    gps_waypoint = factory.Sequence(lambda n: ''.format(n.rjust(3, '0')))
    gps_datetime = datetime.today()
    gps_point_1 = factory.Sequence(lambda n: int(n) + 20)
    gps_point_11 = factory.Sequence(lambda n: int(n) + 20)
    gps_point_2 = factory.Sequence(lambda n: int(n) + 20)
    gps_point_21 = factory.Sequence(lambda n: int(n) + 20)
    #ward_section = factory.Iterator(['A' 'B', 'C', 'D', 'E', 'F'])
    #ward = factory.Iterator(MOCHUDI_WARDS, getter=lambda c: c[0])

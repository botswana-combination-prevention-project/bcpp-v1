import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_household.models import Household


class HouseholdFactory(BaseUuidModelFactory):
    FACTORY_FOR = Household

    household_identifier = factory.Sequence(lambda n: 'household_identifier{0}'.format(n))
    hh_int = 2
    hh_seed = 2
    gps_waypoint = factory.Sequence(lambda n: 'gps_waypoint{0}'.format(n))
    gps_datetime = datetime.today()
    gps_degrees_s = 2
    gps_minutes_s = 2.5
    gps_degrees_e = 2
    gps_minutes_e = 2.5
    gps_target_lon = 2.1234567
    gps_target_lat = 2.1234567
    community = factory.Sequence(lambda n: 'community{0}'.format(n))
    section = factory.Sequence(lambda n: 'section{0}'.format(n))
    sub_section = factory.Sequence(lambda n: 'sub_section{0}'.format(n))
    was_surveyed_previously = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    target = 2

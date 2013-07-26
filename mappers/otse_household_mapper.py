from bhp_map.classes import site_mappers
from base_household_mapper import BaseHouseholdMapper
from bcpp_household.choices import OTSE_SECTIONS, OTSE_SUB_SECTIONS, OTSE_LANDMARKS


class OtseHouseholdMapper(BaseHouseholdMapper):

    map_area = 'otse'

    regions = OTSE_SECTIONS
    sections = OTSE_SUB_SECTIONS

    landmarks = OTSE_LANDMARKS

    gps_center_lat = -24.667415
    gps_center_lon = 25.93537
    radius = 8.699197
    location_boundary = ([-24.67837365156418, 25.840530395507812], [-24.693347103867495, 25.82662582397461], [-24.688980032750187, 25.806884765625],
        [-24.68398890695403, 25.79692840576172], [-24.692099384878524, 25.78319549560547], [-24.691319554166263, 25.77444076538086],
        [-24.681181310871683, 25.772380828857422], [-24.653881943239185, 25.77444076538086], [-24.636398190222742, 25.78088609525048],
        [-24.634225642956554, 25.80328299568498],[-24.634534776496086, 25.82164764404297], [-24.615496736655352, 25.828514099121094],
        [-24.590511092893944, 25.81926212953715], [-24.584592765192067, 25.82714080810547], [-24.56679041341396, 25.820281109619145],
        [-24.554917117007925, 25.83450479867497], [-24.552774718994907, 25.86201171618336], [-24.556803895593834, 25.887908935546875],
        [-24.57366529324845, 25.88275909423828], [-24.57772417981797, 25.86181640625], [-24.57928525502192, 25.9002685546875],
        [-24.565234877943706, 25.895118713378906], [-24.550222426991652, 25.903491498132098], [-24.54493710822876, 25.9332275390625],
        [-24.513225180657674, 25.92771588839014], [-24.502144901210876, 25.972366333007812], [-24.514328108816564, 26.015281677246094],
        [-24.552518387706847, 26.008380010584347], [-24.59099926869428, 25.992630267539425], [-24.62001833371058, 25.993828291022055],
        [-24.64373126244033, 26.021452268223356], [-24.66542640476021, 26.02008819580078], [-24.67414521514242, 25.995154435916902],
        [-24.697558063215652, 26.005325317382812], [-24.714712352236873, 25.979576110839844], [-24.70785092018728, 25.95897674560547],
        [-24.691943419126464, 25.940780639648438], [-24.6931911396771, 25.913658142089844], [-24.69996261331382, 25.88428800448719],
        [-24.68975987810199, 25.863189697265625], [-24.67837365156418, 25.840530395507812])

site_mappers.register(OtseHouseholdMapper)

from bhp_crypto.classes import FieldCryptor
from datetime import date, timedelta
from mochudi_household.choices import WARD_SECTIONS, MOCHUDI_WARDS
from mochudi_household.models import Household
#from bhp_dispatch.helpers import is_dispatched
from bhp_map.choices import ICONS, OTHER_ICONS


def prepare_created_filter():
    date_list_filter = []
    today = date.today() + timedelta(days=0)
    tomorrow = date.today() + timedelta(days=1)
    yesterday = date.today() - timedelta(days=1)
    last_7days = date.today() - timedelta(days=7)
    last_30days = date.today() - timedelta(days=30)

    #created__lt={0},created__gte={1}
    date_list_filter.append(["Any date", ""])
    date_list_filter.append(["Today", "{0},{1}".format(tomorrow, today)])
    date_list_filter.append(["Yesterday", "{0},{1}".format(today, yesterday)])
    date_list_filter.append(["Past 7 days", "{0},{1}".format(tomorrow, last_7days)])
    date_list_filter.append(["Past 30 days", "{0},{1}".format(tomorrow, last_30days)])

    return date_list_filter


def session_to_string(identifiers, new_line=True):
    val = ""
    delim = ", "
    if identifiers:
        for household_identifier in identifiers:
            val = val + household_identifier + delim
    return val


def get_sections():
    return list(mapper.get_choices('WARD_SECTIONS'))

def get_icons():
    return list(ICONS)

def get_other_icons():
    return list(OTHER_ICONS)

def get_regions():
    if not mapper.get_choices('REGIONS'):
        raise MapperError('Mapper choices tuple \'REGIONS\' not defined')
    return sorted([tpl[0] for tpl in list(mapper.get_choices('REGIONS'))])


def make_dictionary(list1, list2):
    #the shortest list should be the first list if the lists do 
    #not have equal number of elements
    sec_icon_dict = {}
    for sec, icon in zip(list1, list2):
        if sec:
            sec_icon_dict[sec] = icon
            
            
        else:
            break
    return sec_icon_dict


def prepare_map_points(items, selected_icon, cart, cart_icon, dipatched_icon='red-circle', selected_section="All"):
    """Returns a list of household identifiers from the given queryset excluding those
    households that have been dispatched
    """
#    item_identifier_field = 'household_identifier'
#    item_region_field = 'ward_section'
    payload = []
    icon_number = 0
    
    if selected_section == "All":
        section_color_code_dict = make_dictionary(get_sections(), get_other_icons())
    else:
        section_color_code_dict = make_dictionary(get_sections(), get_icons())
    
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
                "O", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
       
    for item in items:
        label = str(item.household_identifier)
        cso = ""
        if item.cso_number:
            cso = str("  cso: " + item.cso_number)
        if item.is_dispatched_as_item():
            icon = dipatched_icon
            label = "{0} already dispatched".format(label)
        elif item.household_identifier in cart:
            icon = cart_icon
            label = "{0} in shopping cart waiting to be dispatched".format(label)
        else:
            icon = "blu-circle"
            if selected_section == "All":
                icon = "blu-circle"
                for key_sec, icon_value in section_color_code_dict.iteritems():
                    if item.ward_section == key_sec:
                        if icon_number <= 100:
                            icon = icon_value + str(icon_number)
                            icon_number +=1
                    if icon_number == 100:
                        icon_number = 0
            else:
                for key_sec, icon_value in section_color_code_dict.iteritems():
                    if item.ward_section == key_sec:
                        if icon_number <= 25:
                            icon = icon_value + letters[icon_number]
                            icon_number +=1
                        if icon_number == 25:
                            icon_number = 0
                
        payload.append([item.lon, item.lat, label, icon, cso])
    return payload

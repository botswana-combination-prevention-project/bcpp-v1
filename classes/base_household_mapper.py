# from mapper import Mapper
# 
# 
# class BaseHouseholdMapper(Mapper):
# 
#     def prepare_map_points(self, items, selected_icon, cart, cart_icon, dipatched_icon='red-circle', selected_section="All"):
#         """Returns a list of item identifiers from the given queryset excluding those
#         items that have been dispatched
#         """
#         payload = []
#         icon_number = 0
#         if selected_section == "All":
#             section_color_code_dict = self.make_dictionary(self.get_sections(), self.get_other_icons())
#         else:
#             section_color_code_dict = self.make_dictionary(self.get_sections(), self.get_icons())
#         letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
#                     "O", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
#         for item in items:
#             label = str(item.household_identifier)
#             cso = ""
#             if item.cso_number:
#                 cso = str("  cso: " + item.cso_number)
#             if item.is_dispatched_as_item():
#                 icon = dipatched_icon
#                 label = "{0} already dispatched".format(label)
#             elif item.household_identifier in cart:
#                 icon = cart_icon
#                 label = "{0} in shopping cart waiting to be dispatched".format(label)
#             else:
#                 icon = "blu-circle"
#                 if selected_section == "All":
#                     icon = "blu-circle"
#                     for key_sec, icon_value in section_color_code_dict.iteritems():
#                         if item.ward_section == key_sec:
#                             if icon_number <= 100:
#                                 icon = icon_value + str(icon_number)
#                                 icon_number += 1
#                         if icon_number == 100:
#                             icon_number = 0
#                 else:
#                     for key_sec, icon_value in section_color_code_dict.iteritems():
#                         if item.ward_section == key_sec:
#                             if icon_number <= 25:
#                                 icon = icon_value + letters[icon_number]
#                                 icon_number += 1
#                             if icon_number == 25:
#                                 icon_number = 0
#             payload.append([item.lon, item.lat, label, icon, cso])
#         return payload

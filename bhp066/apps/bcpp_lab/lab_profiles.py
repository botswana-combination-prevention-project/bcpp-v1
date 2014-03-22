from edc.lab.lab_profile.classes import site_lab_profiles

from edc.lab.lab_profile.classes import LabProfile

from .models import Aliquot, AliquotType, Receive, SubjectRequisition, Profile, ProfileItem, Panel


class BaseBcppProfile(LabProfile):
    aliquot_model = Aliquot
    aliquot_type_model = AliquotType
    panel_model = Panel
    receive_model = Receive
    profile_model = Profile
    profile_item_model = ProfileItem


class BcppSubjectProfile(BaseBcppProfile):
    requisition_model = SubjectRequisition
    name = SubjectRequisition._meta.object_name
site_lab_profiles.register(BcppSubjectProfile)

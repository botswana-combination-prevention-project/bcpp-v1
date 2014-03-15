from edc.lab.lab_profile.classes import site_lab_profiles

from edc.lab.lab_profile.classes import LabProfile

from .models import Aliquot, AliquotType, Receive, RBDRequisition, SubjectRequisition, Profile, ProfileItem


class BaseBcppProfile(LabProfile):
    profile_group_name = 'bcpp'
    aliquot_model = Aliquot
    aliquot_type_model = AliquotType
    receive_model = Receive
    profile_model = Profile
    profile_item_model = ProfileItem


class BcppRbdProfile(BaseBcppProfile):
    requisition_model = RBDRequisition
    name = RBDRequisition._meta.object_name
site_lab_profiles.register(BcppRbdProfile)


class BcppSubjectProfile(BaseBcppProfile):
    requisition_model = SubjectRequisition
    name = SubjectRequisition._meta.object_name
site_lab_profiles.register(BcppSubjectProfile)

from edc.lab.lab_profile.classes import site_lab_profiles

from edc.lab.lab_profile.classes import LabProfile

from .models import (Aliquot, AliquotType, Receive, ClinicRequisition, SubjectRequisition,
                     AliquotProfile, AliquotProfileItem, Panel)


class BaseBcppProfile(LabProfile):
    aliquot_model = Aliquot
    aliquot_type_model = AliquotType
    profile_model = AliquotProfile
    profile_item_model = AliquotProfileItem
    receive_model = Receive
    panel_model = Panel


class BcppSubjectProfile(BaseBcppProfile):
    requisition_model = SubjectRequisition
    name = SubjectRequisition._meta.object_name
site_lab_profiles.register(BcppSubjectProfile)


class BaseClinicProfile(LabProfile):
    aliquot_model = Aliquot
    aliquot_type_model = AliquotType
    profile_model = AliquotProfile
    profile_item_model = AliquotProfileItem
    receive_model = Receive
    panel_model = Panel


class ClinicSubjectProfile(BaseClinicProfile):
    requisition_model = ClinicRequisition
    name = ClinicRequisition._meta.object_name
site_lab_profiles.register(ClinicSubjectProfile)

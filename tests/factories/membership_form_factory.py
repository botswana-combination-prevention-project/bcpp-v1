from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_visit.models import MembershipForm

starting_seq_num = 1000


class MembershipFormFactory(BaseUuidModelFactory):
    FACTORY_FOR = MembershipForm

    content_type_map = '1'
    category = 'subject'

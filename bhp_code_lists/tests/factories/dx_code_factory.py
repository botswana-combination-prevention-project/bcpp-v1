from bhp_code_lists.models import DxCode
from base_code_list_factory import BaseCodeListFactory


class DxCodeFactory(BaseCodeListFactory):
    FACTORY_FOR = DxCode

    list_ref = 'DXLISTREF'

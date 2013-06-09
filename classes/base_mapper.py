from bhp_base_model.models import BaseUuidModel
from bhp_map.exceptions import MapperError


class BaseMapper(object):

    def set_item_model_cls(self, cls):
        if not issubclass(cls, BaseUuidModel):
            raise MapperError('Item model class must be a subclass of BaseUuidModel')
        self._item_model_cls = cls

    def get_item_model_cls(self):
        
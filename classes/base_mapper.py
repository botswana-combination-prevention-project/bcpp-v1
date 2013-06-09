from django.utils.encoding import smart_str
from bhp_base_model.models import BaseUuidModel
from bhp_map.exceptions import MapperError


class Mapper(object):

    def __init__(self, *args, **kwargs):
        self._item_model_cls = None
        self._regions = None
        # item_model_cls
        if 'model' in kwargs:
            self.set_item_model_cls(kwargs.get('model'))
        if 'regions' in kwargs:
            self.set_regions(kwargs('regions'))

    def __repr__(self):
        try:
            u = unicode(self)
        except (UnicodeEncodeError, UnicodeDecodeError):
            u = '[Bad Unicode data]'
        return smart_str(u'<%s: %s>' % (self.__class__.__name__, u))

    def set_item_model_cls(self, cls=None):
        if cls:
            if not issubclass(cls, BaseUuidModel):
                raise MapperError('Item model class must be a subclass of BaseUuidModel')
            self._item_model_cls = cls
        else:
            try:
                self._item_model_cls = self.model
            except:
                pass
        if not self._item_model_cls:
            raise MapperError('Attribute \'model\' may not be None (see _item_model_cls) .')

    def get_item_model_cls(self):
        if not self._item_model_cls:
            self.set_item_model_cls()
        return self._item_model_cls

    def set_regions(self, choices_tpl=None):
        if not issubclass(choices_tpl, (tuple, list)):
            raise MapperError('Regions must be a list or choices tuple. Got {0}'.format(choices_tpl))
        self._regions = choices_tpl

    def get_regions(self):
        if not self.choices_tpl:
            self.set_regions()
        return self.choices_tpl

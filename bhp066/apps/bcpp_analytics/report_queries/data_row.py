import collections


class DataRow(object):

    def __init__(self, label, value):
        self.label = label
        self.value = value
        self.is_nested = False
        self.nested_dicts = []
        self._check_for_nesting()

    def is_dict(self):
        return isinstance(self.value, collections.Mapping)

    def _check_for_nesting(self):
        if self.is_dict():
            for key, val in self.value.items():
                if isinstance(val, collections.Mapping):
                    self.is_nested = True
                    self.nested_dicts.append(val)
                    del self.value[key]

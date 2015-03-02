import collections


class DataRow(object):

    def __init__(self, label, value):
        self.label = label
        self.value = value
        self.dicts = self._flatten_nested_dicts()

    def is_dict(self):
        return isinstance(self.value, collections.Mapping)

    def _flatten_nested_dicts(self):
        dicts_list = []
        if self.is_dict():
            dicts_list.append(self.value)
            for key, val in self.value.items():
                if isinstance(val, collections.Mapping):
                    dicts_list.append(val)
                    del self.value[key]
        return dicts_list

    def display_value(self):
        if self.is_dict():
            value_str = ""
            for item in self.dicts:
                value_str += self.print_dict(item)
            return value_str
        else:
            return str(self.value)

    def print_dict(self, a_dict):
        value_str = ""
        for k, v in a_dict.items():
            value_str += str(v) if k == 'header' else " : ".join([k, str(v)])
            value_str += "<br/>"
        return value_str

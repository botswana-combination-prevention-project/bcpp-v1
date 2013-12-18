import collections


class DataRow(object):

    def __init__(self, label, value):
        self.label = label
        self.value = value

    def isdict(self):
        return isinstance(self.value, collections.Mapping)

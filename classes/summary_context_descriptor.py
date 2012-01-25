
class SummaryContextDescriptor(object):

    def __init__(self):
        self.value = {}

    def __get__(self, instance, owner):
        if instance.subject_identifier:
            self.__set__(instance)
        return self.value

    def __set__(self, instance):
        dct = {}
        for attr in dir(instance):
            if not attr[0:1] == '_' and not attr == 'subject_identifier' :
                dct[attr] = getattr(instance, attr)       
        return dct

                

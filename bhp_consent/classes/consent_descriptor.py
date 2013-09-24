#from base_consent import BaseConsent
#
#
#class ConsentDescriptor(object):
#
#    def __init__(self, *args, **kwargs):
#        self.value = None
#
#    def __get__(self, instance, owner):
#        return self.value
#
#    def __set__(self, instance, value):
#        if not isinstance(value, BaseConsent):
#            raise TypeError('Consent must be an instance of BaseConsent.')
#        self.value = value
